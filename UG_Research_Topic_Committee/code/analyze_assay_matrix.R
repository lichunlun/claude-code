# =============================================================================
# analyze_assay_matrix.R -- statistics for Proposal A
#                           (HT-22 differentiation state x viability readout)
#
# !! NOT EXECUTED. READ THIS FIRST. !!
#   R could not be installed in the environment where these deliverables were
#   prepared, so this file has NEVER BEEN RUN. It is a careful port of
#   analyze_assay_matrix.py, which WAS run and whose self-test passes 14/14.
#   Expect to fix syntax or dispatch errors on first use.
#
#   Before trusting any output, run:  Rscript analyze_assay_matrix.R --selftest
#   It should print 14 PASS lines, matching the Python version. If it does not,
#   the Python version is the reference implementation -- use that, or fix this
#   one until the two agree on the same input file.
#
# WHY IT IS SHAPED THIS WAY
#   Proposal A's claim is not "treatment X protects cells". It is "the apparent
#   size of X's protection depends on which readout you use". So:
#     1. The treatment x readout INTERACTION is the primary output, printed
#        first. Main effects come after, de-emphasised.
#     2. Effect sizes with CIs are mandatory. A p-value cannot say "31% under
#        CCK-8, 12% under LDH"; only an effect size can.
#     3. Biological replicates are aggregated by `experiment` BEFORE any test.
#        Technical wells within one experiment are averaged first. Passing
#        technical wells as independent inflates n and makes every p-value
#        wrong, so the script refuses to run on a single-experiment file.
#     4. A non-significant interaction next to a large effect-size spread is
#        flagged as UNDERPOWERED, not as a negative. Interaction terms need
#        several times the n of a main effect; this is the single easiest way
#        to misread this design.
#
# USAGE
#   Rscript analyze_assay_matrix.R --selftest
#   Rscript analyze_assay_matrix.R data/assay_matrix.csv
#   Rscript analyze_assay_matrix.R data/assay_matrix.csv --dose-response
#   Rscript analyze_assay_matrix.R --demo
#
# DEPENDENCIES
#   Base R only (>= 3.6). aov() and nls() are base; nothing to install.
# =============================================================================

options(stringsAsFactors = FALSE, warn = 1)

REQUIRED_COLS <- c("experiment", "plate", "well", "differentiation",
                   "treatment", "glutamate_mM", "readout", "raw_value",
                   "cellfree")
REDUCTION_READOUTS  <- c("CCK8", "MTT", "resazurin")   # dye-reduction based
ORTHOGONAL_READOUTS <- c("LDH")                        # membrane integrity
COND <- c("differentiation", "treatment", "glutamate_mM", "readout")

# ---- Loading and validation -------------------------------------------------
coerce_types <- function(d) {
  flag <- toupper(trimws(as.character(d$cellfree)))
  map <- c("TRUE" = TRUE, "FALSE" = FALSE, "1" = TRUE, "0" = FALSE,
           "T" = TRUE, "F" = FALSE, "YES" = TRUE, "NO" = FALSE)
  d$cellfree <- unname(map[flag])
  if (any(is.na(d$cellfree))) {
    bad <- head(d$well[is.na(d$cellfree)], 5)
    stop("Column 'cellfree' must be TRUE/FALSE; bad well(s): ",
         paste(bad, collapse = ", "))
  }
  for (cc in c("glutamate_mM", "raw_value")) {
    d[[cc]] <- suppressWarnings(as.numeric(d[[cc]]))
    if (any(is.na(d[[cc]]))) stop("Column '", cc, "' has non-numeric values.")
  }
  d
}

load_matrix <- function(path) {
  d <- read.csv(path, check.names = FALSE)
  miss <- setdiff(REQUIRED_COLS, names(d))
  if (length(miss)) {
    stop("Missing required column(s): ", paste(miss, collapse = ", "),
         "\nExpected: ", paste(REQUIRED_COLS, collapse = ", "))
  }
  coerce_types(d)
}

check_replication <- function(d) {
  cells <- d[!d$cellfree, , drop = FALSE]
  n_exp <- length(unique(cells$experiment))
  if (n_exp <= 1) {
    stop("Only one distinct value in 'experiment' for the cell-containing wells.\n",
         "Biological replicates are independent experiments (separate passages,\n",
         "separate platings, separate days) -- not extra wells on one plate. If\n",
         "you really have only one experiment, you do not yet have data to test;\n",
         "collect n >= 3 (ideally 4) and give each its own 'experiment' value.")
  }
  if (n_exp < 3) {
    warning("Only ", n_exp, " independent experiments. Any inference here is ",
            "provisional; aim for n >= 4 before drawing conclusions.")
  }
  invisible(n_exp)
}

# ---- Aggregation: technical wells -> one value per experiment per condition --
aggregate_wells <- function(d) {
  cells <- d[!d$cellfree, , drop = FALSE]
  key <- c("experiment", COND)
  agg <- aggregate(cells$raw_value, by = cells[key], FUN = mean)
  names(agg)[ncol(agg)] <- "value"
  cnt <- aggregate(cells$raw_value, by = cells[key], FUN = length)
  agg$n_wells <- cnt[[ncol(cnt)]]
  agg
}

normalise_to_vehicle <- function(agg) {
  # Normalise WITHIN experiment. Normalising across experiments would hide
  # between-experiment variance, which is the variance that matters.
  out <- list()
  grp <- interaction(agg$experiment, agg$differentiation, agg$readout,
                     drop = TRUE)
  for (lv in levels(grp)) {
    g <- agg[grp == lv, , drop = FALSE]
    ctrl <- g[g$treatment == "vehicle" & g$glutamate_mM == 0, , drop = FALSE]
    if (!nrow(ctrl)) {
      warning("No untreated vehicle control for ", lv, "; rows dropped.")
      next
    }
    base <- mean(ctrl$value)
    if (!is.finite(base) || base == 0) {
      warning("Control value is ", base, " for ", lv, "; rows dropped.")
      next
    }
    g$pct_control <- g$value / base * 100
    out[[lv]] <- g
  }
  if (!length(out)) {
    stop("Nothing could be normalised. Check that every ",
         "experiment x differentiation x readout block has a vehicle / ",
         "glutamate_mM==0 control.")
  }
  do.call(rbind, out)
}

# ---- Effect size ------------------------------------------------------------
hedges_g <- function(a, b) {
  a <- a[is.finite(a)]; b <- b[is.finite(b)]
  n1 <- length(a); n2 <- length(b)
  if (n1 < 2 || n2 < 2) return(c(g = NA, lo = NA, hi = NA))
  sp <- sqrt(((n1 - 1) * var(a) + (n2 - 1) * var(b)) / (n1 + n2 - 2))
  if (!is.finite(sp) || sp == 0) return(c(g = NA, lo = NA, hi = NA))
  d <- (mean(a) - mean(b)) / sp
  J <- 1 - 3 / (4 * (n1 + n2) - 9)                 # small-sample correction
  g <- d * J
  se <- sqrt((n1 + n2) / (n1 * n2) + g^2 / (2 * (n1 + n2 - 2)))
  c(g = g, lo = g - 1.96 * se, hi = g + 1.96 * se)
}

# ---- Primary analysis -------------------------------------------------------
readout_dependence <- function(norm) {
  dmg <- norm[norm$treatment == "vehicle" & norm$glutamate_mM > 0, ,
              drop = FALSE]
  rows <- list()
  trt <- norm[norm$glutamate_mM > 0 & norm$treatment != "vehicle", ,
              drop = FALSE]
  if (!nrow(trt)) return(data.frame())
  key <- unique(trt[c("differentiation", "readout", "treatment")])
  for (i in seq_len(nrow(key))) {
    k <- key[i, ]
    vals <- trt$pct_control[trt$differentiation == k$differentiation &
                              trt$readout == k$readout &
                              trt$treatment == k$treatment]
    base <- dmg$pct_control[dmg$differentiation == k$differentiation &
                              dmg$readout == k$readout]
    if (!length(base)) next
    es <- hedges_g(vals, base)
    rows[[i]] <- data.frame(
      differentiation = k$differentiation, readout = k$readout,
      treatment = k$treatment, n = length(vals),
      mean_pct = round(mean(vals), 1), damage_pct = round(mean(base), 1),
      apparent_protection = round(mean(vals) - mean(base), 1),
      hedges_g = round(es[["g"]], 2), g_lo = round(es[["lo"]], 2),
      g_hi = round(es[["hi"]], 2))
  }
  if (!length(rows)) return(data.frame())
  res <- do.call(rbind, rows)
  res[order(res$differentiation, res$readout, res$treatment), ]
}

readout_spread <- function(dep) {
  if (!nrow(dep)) return(data.frame())
  key <- unique(dep[c("differentiation", "treatment")])
  rows <- list()
  for (i in seq_len(nrow(key))) {
    k <- key[i, ]
    g <- dep[dep$differentiation == k$differentiation &
               dep$treatment == k$treatment, , drop = FALSE]
    if (nrow(g) < 2) next
    red  <- g$apparent_protection[g$readout %in% REDUCTION_READOUTS]
    orth <- g$apparent_protection[g$readout %in% ORTHOGONAL_READOUTS]
    rows[[i]] <- data.frame(
      differentiation = k$differentiation, treatment = k$treatment,
      n_readouts = nrow(g),
      min_protection = min(g$apparent_protection),
      max_protection = max(g$apparent_protection),
      spread = round(max(g$apparent_protection) -
                       min(g$apparent_protection), 1),
      reduction_mean  = if (length(red))  round(mean(red), 1)  else NA,
      orthogonal_mean = if (length(orth)) round(mean(orth), 1) else NA,
      reduction_minus_orthogonal =
        if (length(red) && length(orth)) round(mean(red) - mean(orth), 1) else NA)
  }
  if (!length(rows)) return(data.frame())
  res <- do.call(rbind, rows)
  res[order(-res$spread), ]
}

three_way_anova <- function(norm) {
  sub <- norm[norm$glutamate_mM > 0, , drop = FALSE]
  if (!nrow(sub)) { cat("\n!! No glutamate-treated rows; ANOVA skipped.\n"); return(NULL) }
  for (cc in c("differentiation", "treatment", "readout")) {
    sub[[cc]] <- factor(sub[[cc]])
  }
  terms <- c("differentiation", "treatment", "readout")
  terms <- terms[sapply(terms, function(t) nlevels(sub[[t]]) >= 2)]
  if (length(terms) < 2) {
    cat("\n!! Fewer than two factors vary; ANOVA skipped.\n"); return(NULL)
  }
  fml <- as.formula(paste("pct_control ~", paste(terms, collapse = " * ")))
  fit <- try(aov(fml, data = sub), silent = TRUE)
  if (inherits(fit, "try-error")) {
    cat("\n!! ANOVA could not be fitted. The design is probably not fully",
        "crossed.\n")
    return(NULL)
  }
  summary(fit)[[1]]
}

# ---- Cell-free interference -------------------------------------------------
interference <- function(d) {
  cf <- d[d$cellfree, , drop = FALSE]
  if (!nrow(cf)) return(data.frame())
  rows <- list(); i <- 0
  for (read in unique(cf$readout)) {
    g <- cf[cf$readout == read, , drop = FALSE]
    blank <- g$raw_value[g$treatment == "vehicle"]
    if (!length(blank)) {
      warning("No cell-free vehicle blank for readout=", read, ".")
      next
    }
    b <- mean(blank)
    for (treat in setdiff(unique(g$treatment), "vehicle")) {
      v <- mean(g$raw_value[g$treatment == treat])
      i <- i + 1
      rows[[i]] <- data.frame(
        readout = read, treatment = treat,
        n_wells = sum(g$treatment == treat),
        blank = round(b, 4), compound = round(v, 4),
        signal_over_blank = round(v - b, 4),
        pct_of_blank = if (b != 0) round((v - b) / b * 100, 1) else NA)
    }
  }
  if (!length(rows)) return(data.frame())
  res <- do.call(rbind, rows)
  res[order(-abs(res$pct_of_blank)), ]
}

# ---- Four-parameter logistic ------------------------------------------------
fit_4pl <- function(dose, resp) {
  keep <- dose > 0 & is.finite(resp)
  if (sum(keep) < 5 || length(unique(dose[keep])) < 4) return(NULL)
  x <- dose[keep]; y <- resp[keep]
  st <- list(bottom = min(y), top = max(y), ec50 = median(x), hill = 1)
  fit <- try(nls(y ~ bottom + (top - bottom) / (1 + (x / ec50)^hill),
                 start = st,
                 # ec50 bounded strictly positive: a negative ec50 makes
                 # (x/ec50)^hill a fractional power of a negative number.
                 lower = c(bottom = -Inf, top = -Inf, ec50 = 1e-9, hill = 1e-3),
                 upper = c(bottom = Inf, top = Inf,
                           ec50 = max(x) * 1e3, hill = 50),
                 algorithm = "port",
                 control = nls.control(maxiter = 500, warnOnly = TRUE)),
             silent = TRUE)
  if (inherits(fit, "try-error")) return(NULL)
  co <- try(summary(fit)$coefficients, silent = TRUE)
  if (inherits(co, "try-error") || !("ec50" %in% rownames(co))) return(NULL)
  ec50 <- co["ec50", "Estimate"]; se <- co["ec50", "Std. Error"]
  list(ec50 = ec50,
       ci = if (is.finite(se)) c(ec50 - 1.96 * se, ec50 + 1.96 * se)
            else c(NA, NA))
}

dose_response_table <- function(norm) {
  veh <- norm[norm$treatment == "vehicle", , drop = FALSE]
  key <- unique(veh[c("differentiation", "readout")])
  rows <- list()
  for (i in seq_len(nrow(key))) {
    k <- key[i, ]
    g <- veh[veh$differentiation == k$differentiation &
               veh$readout == k$readout, , drop = FALSE]
    r <- fit_4pl(g$glutamate_mM, g$pct_control)
    rows[[i]] <- if (is.null(r)) {
      data.frame(differentiation = k$differentiation, readout = k$readout,
                 ec50_mM = NA, ci_lo = NA, ci_hi = NA,
                 note = "not enough doses, or fit failed")
    } else {
      data.frame(differentiation = k$differentiation, readout = k$readout,
                 ec50_mM = round(r$ec50, 3), ci_lo = round(r$ci[1], 3),
                 ci_hi = round(r$ci[2], 3), note = "")
    }
  }
  do.call(rbind, rows)
}

ci_overlap <- function(a, b) {
  if (any(!is.finite(c(a, b)))) return(NA)
  !(a[2] < b[1] || b[2] < a[1])
}

# ---- Report -----------------------------------------------------------------
report <- function(d, path, want_dose = FALSE) {
  bar <- strrep("=", 78)
  cat("\n", bar, "\nASSAY MATRIX ANALYSIS  (Proposal A)\nsource: ", path,
      "\n", bar, "\n", sep = "")

  cells <- d[!d$cellfree, , drop = FALSE]
  n_exp <- length(unique(cells$experiment))
  cat(sprintf("\nwells: %d total, %d with cells, %d cell-free\n",
              nrow(d), nrow(cells), nrow(d) - nrow(cells)))
  cat("independent experiments (n): ", n_exp, "\n", sep = "")
  cat("readouts: ", paste(sort(unique(cells$readout)), collapse = ", "),
      "\n", sep = "")

  norm <- normalise_to_vehicle(aggregate_wells(d))

  cat("\n", bar, "\nPRIMARY OUTPUT -- does the answer depend on the readout?\n",
      bar, "\n", sep = "")
  dep <- readout_dependence(norm)
  spread <- data.frame()
  if (!nrow(dep)) {
    cat("  (no glutamate-treated, non-vehicle conditions found)\n")
  } else {
    cat("\nApparent protection by treatment and readout",
        "(percentage points vs damage control):\n")
    print(dep, row.names = FALSE)
    spread <- readout_spread(dep)
    cat("\n** THE FIGURE 5 TABLE ** -- spread of the same effect across readouts:\n")
    print(spread, row.names = FALSE)
    if (nrow(spread) && is.finite(spread$spread[1])) {
      cat(sprintf(paste0("\n  Largest readout-dependence: %s in %s cells ",
                         "varies by %.1f percentage points\n  depending only ",
                         "on which viability assay was used.\n"),
                  spread$treatment[1], spread$differentiation[1],
                  spread$spread[1]))
    }
  }

  av <- three_way_anova(norm)
  if (!is.null(av)) {
    rn <- trimws(rownames(av))
    inter <- grep(":", rn)
    cat("\nANOVA -- interaction terms first (these are the result):\n")
    if (length(inter)) print(av[inter, , drop = FALSE]) else
      cat("  (no interaction terms estimable in this design)\n")
    main <- setdiff(seq_along(rn), c(inter, grep("^Residuals$", rn)))
    if (length(main)) {
      cat("\n  main effects (secondary):\n")
      print(av[main, , drop = FALSE])
    }
    # Power caveat -- see header note 4.
    tr <- grep("treatment", rn[inter], value = TRUE)
    tr <- grep("readout", tr, value = TRUE)
    if (length(tr) && nrow(spread) && spread$spread[1] >= 10) {
      p <- av[match(tr[1], rn), "Pr(>F)"]
      if (is.finite(p) && p > 0.05) {
        cat(sprintf(paste0(
          "\n  !! CAUTION: the treatment x readout interaction is not ",
          "significant (p = %.2f),\n     yet the largest observed readout ",
          "spread is %.1f percentage points at n = %d.\n     An interaction ",
          "term needs several times the n of a main effect. Do NOT read\n",
          "     this as 'readout does not matter' -- it is an underpowered ",
          "test sitting next\n     to a large descriptive effect. Report the ",
          "effect-size table as the primary\n     result, state the ",
          "interaction was underpowered, and use the observed\n     variance ",
          "to compute the n a confirmatory test would need.\n"),
          p, spread$spread[1], n_exp))
      }
    }
  }

  cat("\n", bar,
      "\nCELL-FREE INTERFERENCE -- what the compound does to the dye alone\n",
      bar, "\n", sep = "")
  inf <- interference(d)
  if (!nrow(inf)) {
    cat("\n  No cell-free wells in this file. This is the cheapest and most\n",
        "  decisive control in the whole proposal -- medium + compound + dye,\n",
        "  no cells. Run it before anything else.\n", sep = "")
  } else {
    cat("\n"); print(inf, row.names = FALSE)
    big <- inf[is.finite(inf$pct_of_blank) & abs(inf$pct_of_blank) > 10, ,
               drop = FALSE]
    if (nrow(big)) {
      cat("\n  ** Compounds altering the dye signal by >10% of blank with NO",
          "cells present:\n")
      for (i in seq_len(nrow(big))) {
        cat(sprintf("     %-12s %-10s %+.1f%% of blank\n",
                    big$treatment[i], big$readout[i], big$pct_of_blank[i]))
      }
      cat("\n  Any apparent protection by these compounds in the same readout",
          "is inflated\n  by an amount this table bounds.\n")
    } else {
      cat("\n  No compound shifts any dye by >10% of blank. The interference",
          "axis is weak\n  in this dataset -- report that as a negative rather",
          "than dropping it.\n")
    }
  }

  if (want_dose) {
    cat("\n", bar, "\nDOSE-RESPONSE (4PL)\n", bar, "\n\n", sep = "")
    dr <- dose_response_table(norm)
    print(dr, row.names = FALSE)
    ok <- dr[dr$note == "", , drop = FALSE]
    for (read in unique(ok$readout)) {
      g <- ok[ok$readout == read, , drop = FALSE]
      if (length(unique(g$differentiation)) == 2) {
        u <- g[g$differentiation == "undiff", ][1, ]
        v <- g[g$differentiation == "diff", ][1, ]
        ov <- ci_overlap(c(u$ci_lo, u$ci_hi), c(v$ci_lo, v$ci_hi))
        verdict <- if (is.na(ov)) "CI not estimable" else if (ov)
          "CIs OVERLAP -> differentiation effect not resolved" else
          "CIs separate -> differentiation effect resolved"
        cat(sprintf("\n  %s: undiff EC50 %s vs diff %s mM -- %s\n",
                    read, u$ec50_mM, v$ec50_mM, verdict))
      }
    }
  }

  cat("\n", bar, "\n", sep = "")
  cat("Reminder: the claim this analysis supports is about THIS cell line",
      "under THESE\nconditions. Effect sizes and CIs above are reportable;",
      "p-values alone are not.\nNo conclusion here licenses a statement about",
      "neurons in vivo.\n")
  cat(bar, "\n", sep = "")

  dest <- file.path(dirname(normalizePath(path, mustWork = FALSE)),
                    "assay_matrix_normalised.csv")
  write.csv(norm, dest, row.names = FALSE)
  cat("\nNormalised per-experiment data written to: ", dest, "\n\n", sep = "")
  invisible(norm)
}

# ---- Simulated data with a KNOWN planted artifact ---------------------------
make_fake <- function(seed = 7) {
  set.seed(seed)
  readouts <- c("CCK8", "MTT", "resazurin", "LDH")
  treatments <- c("vehicle", "MK801", "DTT")
  true_prot <- c("diff.MK801" = 25, "undiff.MK801" = 2,
                 "diff.DTT" = 3, "undiff.DTT" = 10)
  dye_art <- c(CCK8 = 15, MTT = 18, resazurin = 6, LDH = 0)
  rows <- list(); i <- 0
  for (exp in paste0("exp", 1:4)) {
    for (dff in c("undiff", "diff")) for (tr in treatments)
      for (rd in readouts) for (glut in c(0, 5)) {
        base <- 100
        if (glut > 0) {
          base <- base - 60
          key <- paste(dff, tr, sep = ".")
          if (key %in% names(true_prot)) base <- base + true_prot[[key]]
          if (tr != "vehicle" && rd %in% REDUCTION_READOUTS)
            base <- base + dye_art[[rd]]
        }
        for (w in 1:3) {
          i <- i + 1
          rows[[i]] <- data.frame(
            experiment = exp, plate = paste(exp, rd, sep = "_"),
            well = paste0(substr(toupper(dff), 1, 1), w),
            differentiation = dff, treatment = tr, glutamate_mM = glut,
            readout = rd, raw_value = max(rnorm(1, base, 6), 0.1) / 100,
            cellfree = "FALSE")
        }
      }
    for (dff in c("undiff", "diff")) for (rd in readouts) {
      ec50 <- if (dff == "diff") 1 else 8
      for (glut in c(0.25, 0.5, 1, 2, 4, 8, 16)) for (w in 1:2) {
        i <- i + 1
        resp <- 100 / (1 + (glut / ec50)^1.6)
        rows[[i]] <- data.frame(
          experiment = exp, plate = paste("dr", exp, rd, sep = "_"),
          well = paste0("D", w), differentiation = dff, treatment = "vehicle",
          glutamate_mM = glut, readout = rd,
          raw_value = max(rnorm(1, resp, 5), 0.1) / 100, cellfree = "FALSE")
      }
    }
    for (tr in treatments) for (rd in readouts) {
      base <- 0.08 + if (tr == "DTT" && rd %in% REDUCTION_READOUTS)
        dye_art[[rd]] / 100 else 0
      for (w in 1:3) {
        i <- i + 1
        rows[[i]] <- data.frame(
          experiment = exp, plate = paste0("cf_", exp), well = paste0("F", w),
          differentiation = "undiff", treatment = tr, glutamate_mM = 0,
          readout = rd, raw_value = max(rnorm(1, base, 0.01), 0.001),
          cellfree = "TRUE")
      }
    }
  }
  do.call(rbind, rows)
}

# ---- Self-test --------------------------------------------------------------
selftest <- function() {
  d <- coerce_types(make_fake())
  checks <- list()
  add <- function(name, ok) checks[[length(checks) + 1]] <<- list(name, isTRUE(ok))

  add("simulated data has every required column",
      length(setdiff(REQUIRED_COLS, names(d))) == 0)
  check_replication(d)
  add("accepts data with 4 independent experiments", TRUE)
  one <- d[d$experiment == "exp1", , drop = FALSE]
  add("rejects single-experiment data",
      inherits(try(check_replication(one), silent = TRUE), "try-error"))

  norm <- normalise_to_vehicle(aggregate_wells(d))
  ctl <- norm$pct_control[norm$treatment == "vehicle" & norm$glutamate_mM == 0]
  add("normalisation produces ~100 for untreated controls",
      abs(mean(ctl) - 100) < 1)

  inf <- interference(d)
  dtt <- inf[inf$treatment == "DTT", , drop = FALSE]
  add("cell-free arm flags the planted DTT dye artifact",
      all(dtt$pct_of_blank[dtt$readout %in% REDUCTION_READOUTS] > 50))
  add("cell-free arm leaves LDH clean",
      abs(dtt$pct_of_blank[dtt$readout == "LDH"][1]) < 20)

  dep <- readout_dependence(norm); spread <- readout_spread(dep)
  du <- spread[spread$treatment == "DTT" & spread$differentiation == "undiff", ]
  add("recovers readout-dependence for the artifact compound",
      nrow(du) > 0 && du$spread[1] > 8)
  add("reduction-minus-orthogonal is positive for DTT",
      nrow(du) > 0 && du$reduction_minus_orthogonal[1] > 5)
  mk <- dep[dep$treatment == "MK801" & dep$differentiation == "diff" &
              dep$readout == "LDH", ]
  add("recovers true MK801 protection in diff cells (LDH)",
      nrow(mk) > 0 && mk$apparent_protection[1] > 15)

  es <- hedges_g(c(10, 11, 12, 13), c(1, 2, 3, 4))
  add("Hedges' g positive with non-overlapping CI",
      es[["g"]] > 2 && es[["lo"]] > 0)
  add("Hedges' g returns NA for n<2", is.na(hedges_g(1, 2)[["g"]]))

  f <- fit_4pl(c(0.25, .5, 1, 2, 4, 8, 16), c(98, 95, 80, 50, 22, 8, 3))
  add("4PL fit recovers EC50 near 2",
      !is.null(f) && f$ec50 > 1 && f$ec50 < 3.5)
  dr <- dose_response_table(norm)
  add("dose-response table fits both differentiation states",
      length(unique(dr$differentiation[dr$note == ""])) == 2)

  av <- three_way_anova(norm)
  add("ANOVA yields at least one interaction term",
      !is.null(av) && any(grepl(":", trimws(rownames(av)))))

  for (ck in checks)
    cat(sprintf("  [%s] %s\n", if (ck[[2]]) "PASS" else "FAIL", ck[[1]]))
  nfail <- sum(!vapply(checks, `[[`, logical(1), 2))
  cat(sprintf("\n%d/%d checks passed\n", length(checks) - nfail, length(checks)))
  if (nfail) {
    cat("failed: ",
        paste(vapply(Filter(function(x) !x[[2]], checks), `[[`,
                     character(1), 1), collapse = "; "), "\n")
  }
  invisible(as.integer(nfail > 0))
}

# ---- Entry point ------------------------------------------------------------
main <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  if ("--selftest" %in% args) { q(status = selftest(), save = "no") }
  if ("--demo" %in% args) {
    tmp <- tempfile(fileext = ".csv")
    write.csv(make_fake(), tmp, row.names = FALSE)
    d <- load_matrix(tmp); check_replication(d)
    report(d, tmp, want_dose = TRUE)
    unlink(tmp)
    q(status = 0, save = "no")
  }
  csv <- args[!grepl("^--", args)][1]
  if (is.na(csv)) {
    cat("Usage:\n",
        "  Rscript analyze_assay_matrix.R --selftest\n",
        "  Rscript analyze_assay_matrix.R --demo\n",
        "  Rscript analyze_assay_matrix.R <file.csv> [--dose-response]\n", sep = "")
    q(status = 2, save = "no")
  }
  if (!file.exists(csv)) stop("File not found: ", csv)
  d <- load_matrix(csv); check_replication(d)
  report(d, csv, want_dose = "--dose-response" %in% args)
  q(status = 0, save = "no")
}

if (!interactive()) main()
