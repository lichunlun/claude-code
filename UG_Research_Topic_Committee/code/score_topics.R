# =============================================================================
# score_topics.R  --  Transparent, reproducible scoring of candidate research
#                     topics for an undergraduate original-research project.
#
# WHY THIS SCRIPT EXISTS
#   The committee's 100-point rubric is easy to apply dishonestly: you pick the
#   topic you like, then back-fill the sub-scores. This script forces the
#   opposite order. Sub-scores live in a flat CSV, the weights live in one
#   place, and the ranking is computed. If you want to change the answer you
#   have to change a number you can be argued with about.
#
#   It also keeps four DIFFERENT success probabilities separate, because they
#   are genuinely different things and conflating them is the single most
#   common planning error in undergraduate projects:
#       p_exec   = P(the experiments can physically be completed)
#       p_paper  = P(the results, whatever they are, assemble into a paper)
#       p_accept = P(that paper is accepted by an SCI-indexed journal)
#       sci_val  = scientific value, which is NOT a probability and must not
#                  be multiplied with them
#
#   These are elicited judgements, not measurements. They are recorded so they
#   can be criticised, not so they can be believed. See the
#   `confidence` column: anything marked "low" should be read as a placeholder.
#
# USAGE
#   Rscript score_topics.R [path/to/topic_scores.csv]
#   Defaults to ../data/topic_scores.csv relative to this script.
#
# DEPENDENCIES
#   Base R only (>= 3.6). No packages required, deliberately: this must run on
#   a student laptop with no setup.
# =============================================================================

options(stringsAsFactors = FALSE)

# ---- 1. The rubric -----------------------------------------------------------
# Weights are the committee's, and must sum to 100.
WEIGHTS <- c(
  importance      = 15,  # Significance of the scientific question
  novelty         = 20,  # Genuine novelty (not the 6 pseudo-novelty traps)
  fit_resources   = 15,  # Fit to the student's ACTUAL platform
  operability     = 15,  # Can the experiments really be run, by this person
  finish_6_12mo   = 10,  # Probability of finishing in 6-12 months
  sci_potential   = 15,  # SCI publication potential (NOT impact factor)
  negative_value  = 5,   # Scientific value of the negative result
  ug_contribution = 5    # Room for independent undergraduate contribution
)

stopifnot(sum(WEIGHTS) == 100)

# Each dimension is scored 0-10 in the CSV, then scaled by its weight.
SCORE_MAX <- 10

# ---- 2. Load ------------------------------------------------------------------
args <- commandArgs(trailingOnly = TRUE)
default_csv <- file.path(dirname(sub("^--file=", "", grep("^--file=",
                          commandArgs(trailingOnly = FALSE), value = TRUE)[1])),
                         "..", "data", "topic_scores.csv")
csv_path <- if (length(args) >= 1) args[1] else default_csv

if (!file.exists(csv_path)) {
  stop(sprintf(paste0(
    "Score file not found: %s\n",
    "Create it with the columns listed in the header of this script, or pass\n",
    "a path as the first argument."), csv_path))
}

d <- read.csv(csv_path, check.names = FALSE)

required <- c("id", "short_name", names(WEIGHTS),
              "p_exec", "p_paper", "p_accept",
              "novelty_rating", "evidence_rating", "overlap_risk",
              "confidence")
missing <- setdiff(required, names(d))
if (length(missing)) {
  stop("Missing required column(s): ", paste(missing, collapse = ", "))
}

# ---- 3. Validate --------------------------------------------------------------
# Fail loudly on out-of-range input rather than silently producing a ranking.
for (nm in names(WEIGHTS)) {
  bad <- which(is.na(d[[nm]]) | d[[nm]] < 0 | d[[nm]] > SCORE_MAX)
  if (length(bad)) {
    stop(sprintf("Column '%s' has out-of-range values (must be 0-%d) in row(s): %s",
                 nm, SCORE_MAX, paste(d$id[bad], collapse = ", ")))
  }
}
for (nm in c("p_exec", "p_paper", "p_accept")) {
  bad <- which(is.na(d[[nm]]) | d[[nm]] < 0 | d[[nm]] > 1)
  if (length(bad)) {
    stop(sprintf("Column '%s' must be a probability in [0,1]; bad row(s): %s",
                 nm, paste(d$id[bad], collapse = ", ")))
  }
}
ok_hml <- function(x) all(toupper(x) %in% c("H", "M", "L"))
for (nm in c("novelty_rating", "evidence_rating", "overlap_risk")) {
  if (!ok_hml(d[[nm]])) stop(sprintf("Column '%s' must be H, M or L.", nm))
}

# ---- 4. Score -----------------------------------------------------------------
weighted <- sapply(names(WEIGHTS), function(nm) d[[nm]] / SCORE_MAX * WEIGHTS[[nm]])
if (is.null(dim(weighted))) weighted <- matrix(weighted, nrow = nrow(d),
                                               dimnames = list(NULL, names(WEIGHTS)))
d$total <- round(rowSums(weighted), 1)

# Composite pipeline probability: the chance this ends as an accepted paper.
# Deliberately a product -- the three stages are sequential gates, and the
# product is always smaller than any single stage, which is the honest result.
d$p_published <- round(d$p_exec * d$p_paper * d$p_accept, 3)

# A topic can score well on the rubric and still be a bad bet, or score
# modestly and be a good bet. Flag the divergence instead of hiding it.
d$rubric_rank <- rank(-d$total, ties.method = "min")
d$pipeline_rank <- rank(-d$p_published, ties.method = "min")
d$rank_divergence <- d$pipeline_rank - d$rubric_rank

# Penalty flags: things that should stop a topic regardless of total score.
d$flag_overlap  <- ifelse(toupper(d$overlap_risk) == "H", "HIGH-OVERLAP", "")
d$flag_evidence <- ifelse(toupper(d$evidence_rating) == "L", "THIN-EVIDENCE", "")
d$flag_lowconf  <- ifelse(tolower(d$confidence) == "low", "LOW-CONFIDENCE", "")
d$flags <- trimws(paste(d$flag_overlap, d$flag_evidence, d$flag_lowconf))

# ---- 5. Report ----------------------------------------------------------------
cat("\n", strrep("=", 78), "\n", sep = "")
cat("CANDIDATE TOPIC SCORING\n")
cat("source: ", normalizePath(csv_path), "\n", sep = "")
cat(strrep("=", 78), "\n\n", sep = "")

cat("Rubric weights (sum = 100):\n")
for (nm in names(WEIGHTS)) cat(sprintf("  %-16s %3d\n", nm, WEIGHTS[[nm]]))
cat("\n")

ord <- order(-d$total)
out <- d[ord, c("id", "short_name", "total", "p_exec", "p_paper", "p_accept",
                "p_published", "novelty_rating", "overlap_risk", "flags")]
names(out) <- c("ID", "Topic", "Score", "pExec", "pPaper", "pAccept",
                "pPublished", "Nov", "Ovl", "Flags")
print(out, row.names = FALSE, right = FALSE)

cat("\n-- Dimension detail (weighted points) --\n")
det <- cbind(id = d$id[ord], round(as.data.frame(weighted)[ord, , drop = FALSE], 1))
print(det, row.names = FALSE)

cat("\n-- Rank divergence (pipeline rank minus rubric rank) --\n")
cat("   Positive = scores better on the rubric than its realistic odds justify.\n")
cat("   Negative = a better bet than its rubric score suggests.\n\n")
div <- d[order(-abs(d$rank_divergence)),
         c("id", "short_name", "rubric_rank", "pipeline_rank", "rank_divergence")]
print(head(div, 10), row.names = FALSE, right = FALSE)

cat("\n-- Topics carrying a blocking flag --\n")
fl <- d[d$flags != "", c("id", "short_name", "total", "flags")]
if (nrow(fl) == 0) cat("   none\n") else print(fl, row.names = FALSE, right = FALSE)

cat("\nNOTE: every number above is an elicited judgement, not a measurement.\n")
cat("      p_published is a product of three subjective probabilities and is\n")
cat("      therefore the least reliable figure in the table. Use it to compare\n")
cat("      topics against each other, never as a forecast of success.\n\n")

invisible(write.csv(d[ord, ], file.path(dirname(csv_path), "topic_scores_ranked.csv"),
                    row.names = FALSE))
cat("Ranked table written to: ",
    file.path(dirname(csv_path), "topic_scores_ranked.csv"), "\n\n", sep = "")
