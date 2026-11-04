#!/usr/bin/env python3
"""
analyze_assay_matrix.py -- statistics for Proposal A (HT-22 differentiation state
x viability readout).

WHAT THIS DOES, AND WHY IT IS SHAPED THIS WAY
---------------------------------------------
Proposal A's central claim is not "treatment X protects cells". It is
"the apparent size of X's protection depends on which readout you use".
That makes the treatment x readout INTERACTION the result, not a nuisance
term. Three things in this script follow from that:

  1. The interaction is printed first and labelled as the primary output.
     Main effects are printed after, de-emphasised.

  2. Effect sizes with confidence intervals are mandatory. A p-value cannot
     express "the effect is 31% under CCK-8 and 12% under LDH" -- only an
     effect size can. The script refuses to print a p-value without one.

  3. Biological replicates are aggregated by the `experiment` column before
     any test. Technical replicate wells within one experiment are averaged
     first. If you pass technical replicates as if they were independent, n
     is inflated and every p-value is wrong; the script checks for this and
     errors out rather than quietly doing it.

It also does the cell-free interference correction, which is the number that
Figure 5 is made of: how much of the apparent protection survives once you
subtract what the compound does to the dye with no cells present.

INPUT
-----
Long-format CSV, one row per well:

    experiment       independent experiment id (= the unit of n), e.g. exp1
    plate            plate id
    well             well position, e.g. A1
    differentiation  undiff | diff
    treatment        vehicle | MK801 | memantine | DTT | Fer1 | ...
    glutamate_mM     numeric, 0 for none
    readout          CCK8 | MTT | resazurin | LDH
    raw_value        numeric reading
    cellfree         TRUE | FALSE

USAGE
-----
    python3 analyze_assay_matrix.py --selftest
    python3 analyze_assay_matrix.py data/assay_matrix.csv
    python3 analyze_assay_matrix.py data/assay_matrix.csv --dose-response

DEPENDENCIES
------------
numpy, pandas, scipy, statsmodels.
    pip install numpy pandas scipy statsmodels
"""

from __future__ import annotations

import argparse
import itertools
import os
import sys
import warnings

import numpy as np
import pandas as pd

REQUIRED_COLS = [
    "experiment", "plate", "well", "differentiation", "treatment",
    "glutamate_mM", "readout", "raw_value", "cellfree",
]

REDUCTION_READOUTS = {"CCK8", "MTT", "resazurin"}   # dye-reduction based
ORTHOGONAL_READOUTS = {"LDH"}                        # membrane integrity


# ---------------------------------------------------------------------------
# Loading and validation
# ---------------------------------------------------------------------------
def coerce_types(d: pd.DataFrame) -> pd.DataFrame:
    """Coerce the flag and numeric columns. Shared by load() and the self-test,
    so the self-test exercises the same coercion a real file goes through."""
    d = d.copy()
    d["cellfree"] = (d["cellfree"].astype(str).str.strip().str.upper()
                     .map({"TRUE": True, "FALSE": False, "1": True, "0": False,
                           "T": True, "F": False, "YES": True, "NO": False}))
    if d["cellfree"].isna().any():
        bad = d.loc[d["cellfree"].isna(), "well"].tolist()[:5]
        raise SystemExit(f"Column 'cellfree' must be TRUE/FALSE; bad well(s): {bad}")
    d["cellfree"] = d["cellfree"].astype(bool)

    for c in ("glutamate_mM", "raw_value"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
        if d[c].isna().any():
            raise SystemExit(f"Column '{c}' has non-numeric values.")
    return d


def load(path: str) -> pd.DataFrame:
    d = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLS if c not in d.columns]
    if missing:
        raise SystemExit(f"Missing required column(s): {', '.join(missing)}\n"
                         f"Expected: {', '.join(REQUIRED_COLS)}")
    return coerce_types(d)


def check_replication(d: pd.DataFrame) -> None:
    """Refuse to analyse data where n would be inflated by technical replicates.

    The failure mode this catches: a student runs one experiment with six
    wells per condition and reports n=6. The wells are not independent, so
    every p-value downstream is too small. We cannot detect this with
    certainty, but a single `experiment` value across the whole file is a
    reliable signature of it.
    """
    cells = d.loc[~d["cellfree"]]
    n_exp = cells["experiment"].nunique()
    if n_exp <= 1:
        raise SystemExit(
            "Only one distinct value in 'experiment' for the cell-containing "
            "wells.\n"
            "Biological replicates are independent experiments (separate "
            "passages, separate\nplatings, separate days) -- not extra wells "
            "on one plate. If you really have\nonly one experiment, you do "
            "not yet have data to test; collect n >= 3 (ideally 4)\nand give "
            "each its own 'experiment' value."
        )
    if n_exp < 3:
        warnings.warn(
            f"Only {n_exp} independent experiments. Any inference here is "
            "provisional; aim for n >= 4 before drawing conclusions.",
            stacklevel=2,
        )


# ---------------------------------------------------------------------------
# Aggregation: technical wells -> one value per experiment per condition
# ---------------------------------------------------------------------------
COND = ["differentiation", "treatment", "glutamate_mM", "readout"]


def aggregate(d: pd.DataFrame) -> pd.DataFrame:
    cells = d.loc[~d["cellfree"]].copy()
    agg = (cells.groupby(["experiment"] + COND, as_index=False)
                .agg(value=("raw_value", "mean"),
                     n_wells=("raw_value", "size")))
    return agg


def normalise_to_vehicle(agg: pd.DataFrame) -> pd.DataFrame:
    """Express each condition as % of its own experiment's untreated control.

    Normalising within experiment (not across) is what makes independent
    experiments comparable; normalising across experiments would hide
    between-experiment variance, which is the variance that matters.
    """
    out = []
    for (exp, diff, read), g in agg.groupby(
            ["experiment", "differentiation", "readout"]):
        ctrl = g[(g["treatment"] == "vehicle") & (g["glutamate_mM"] == 0)]
        if ctrl.empty:
            warnings.warn(
                f"No untreated vehicle control for experiment={exp}, "
                f"differentiation={diff}, readout={read}; "
                "those rows cannot be normalised and are dropped.",
                stacklevel=2)
            continue
        base = ctrl["value"].mean()
        if not np.isfinite(base) or base == 0:
            warnings.warn(f"Control value is {base} for {exp}/{diff}/{read}; "
                          "rows dropped.", stacklevel=2)
            continue
        g = g.copy()
        g["pct_control"] = g["value"] / base * 100.0
        out.append(g)
    if not out:
        raise SystemExit("Nothing could be normalised. Check that every "
                         "experiment x differentiation x readout block has a "
                         "vehicle / glutamate_mM==0 control.")
    return pd.concat(out, ignore_index=True)


# ---------------------------------------------------------------------------
# Effect size
# ---------------------------------------------------------------------------
def hedges_g(a: np.ndarray, b: np.ndarray) -> tuple[float, float, float]:
    """Hedges' g with a 95% CI. Returns (g, lo, hi)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        return (np.nan, np.nan, np.nan)
    s1, s2 = a.var(ddof=1), b.var(ddof=1)
    sp = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
    if sp == 0:
        return (np.nan, np.nan, np.nan)
    d = (a.mean() - b.mean()) / sp
    J = 1 - 3 / (4 * (n1 + n2) - 9)          # small-sample correction
    g = d * J
    se = np.sqrt((n1 + n2) / (n1 * n2) + g ** 2 / (2 * (n1 + n2 - 2)))
    return (g, g - 1.96 * se, g + 1.96 * se)


# ---------------------------------------------------------------------------
# Primary analysis: the interaction
# ---------------------------------------------------------------------------
def three_way_anova(norm: pd.DataFrame) -> pd.DataFrame | None:
    try:
        import statsmodels.api as sm
        from statsmodels.formula.api import ols
    except ImportError:
        print("\n!! statsmodels is not installed, so the ANOVA table is "
              "skipped.\n   pip install statsmodels\n   The effect-size "
              "tables below do not depend on it.")
        return None

    sub = norm[(norm["glutamate_mM"] > 0)].copy()
    if sub.empty:
        print("\n!! No glutamate-treated rows; ANOVA skipped.")
        return None
    for c in ("differentiation", "treatment", "readout"):
        sub[c] = sub[c].astype("category")

    levels = {c: sub[c].nunique() for c in
              ("differentiation", "treatment", "readout")}
    terms = [c for c, k in levels.items() if k >= 2]
    if len(terms) < 2:
        print(f"\n!! Fewer than two factors vary ({levels}); ANOVA skipped.")
        return None

    formula = "pct_control ~ " + " * ".join(f"C({t})" for t in terms)
    try:
        model = ols(formula, data=sub).fit()
        return sm.stats.anova_lm(model, typ=2)
    except Exception as exc:                        # noqa: BLE001
        print(f"\n!! ANOVA could not be fitted ({exc}). This usually means the "
              "design is not\n   fully crossed -- some factor combination has "
              "no observations.")
        return None


def readout_dependence(norm: pd.DataFrame) -> pd.DataFrame:
    """THE primary table: apparent protection per treatment, per readout.

    This is the content of Figure 5. For each differentiation state and
    treatment, it reports apparent protection under each readout, so the
    spread across readouts can be read directly.
    """
    rows = []
    dmg = norm[(norm["treatment"] == "vehicle") & (norm["glutamate_mM"] > 0)]
    for (diff, read), g in norm.groupby(["differentiation", "readout"]):
        base = dmg[(dmg["differentiation"] == diff) & (dmg["readout"] == read)]
        if base.empty:
            continue
        base_vals = base["pct_control"].to_numpy()
        for treat, gt in g[(g["glutamate_mM"] > 0) &
                           (g["treatment"] != "vehicle")].groupby("treatment"):
            vals = gt["pct_control"].to_numpy()
            gval, lo, hi = hedges_g(vals, base_vals)
            rows.append(dict(
                differentiation=diff, readout=read, treatment=treat,
                n=len(vals),
                mean_pct=round(float(vals.mean()), 1),
                damage_pct=round(float(base_vals.mean()), 1),
                apparent_protection=round(
                    float(vals.mean() - base_vals.mean()), 1),
                hedges_g=round(gval, 2) if np.isfinite(gval) else np.nan,
                g_lo=round(lo, 2) if np.isfinite(lo) else np.nan,
                g_hi=round(hi, 2) if np.isfinite(hi) else np.nan,
            ))
    return pd.DataFrame(rows)


def readout_spread(dep: pd.DataFrame) -> pd.DataFrame:
    """How much does the answer change with the readout? One row per treatment."""
    rows = []
    for (diff, treat), g in dep.groupby(["differentiation", "treatment"]):
        if len(g) < 2:
            continue
        red = g[g["readout"].isin(REDUCTION_READOUTS)]["apparent_protection"]
        orth = g[g["readout"].isin(ORTHOGONAL_READOUTS)]["apparent_protection"]
        rows.append(dict(
            differentiation=diff, treatment=treat,
            n_readouts=len(g),
            min_protection=g["apparent_protection"].min(),
            max_protection=g["apparent_protection"].max(),
            spread=round(float(g["apparent_protection"].max()
                               - g["apparent_protection"].min()), 1),
            reduction_mean=round(float(red.mean()), 1) if len(red) else np.nan,
            orthogonal_mean=round(float(orth.mean()), 1) if len(orth) else np.nan,
            reduction_minus_orthogonal=(
                round(float(red.mean() - orth.mean()), 1)
                if len(red) and len(orth) else np.nan),
        ))
    return pd.DataFrame(rows).sort_values("spread", ascending=False)


# ---------------------------------------------------------------------------
# Cell-free interference correction -- the Figure 5 number
# ---------------------------------------------------------------------------
def interference(d: pd.DataFrame) -> pd.DataFrame:
    """Dye reduction produced by each compound with NO cells present."""
    cf = d.loc[d["cellfree"]].copy()
    if cf.empty:
        return pd.DataFrame()
    rows = []
    for read, g in cf.groupby("readout"):
        blank = g[g["treatment"] == "vehicle"]["raw_value"]
        if blank.empty:
            warnings.warn(f"No cell-free vehicle blank for readout={read}; "
                          "interference cannot be expressed relative to blank.",
                          stacklevel=2)
            continue
        b = float(blank.mean())
        for treat, gt in g[g["treatment"] != "vehicle"].groupby("treatment"):
            v = float(gt["raw_value"].mean())
            rows.append(dict(
                readout=read, treatment=treat, n_wells=len(gt),
                blank=round(b, 4), compound=round(v, 4),
                signal_over_blank=round(v - b, 4),
                pct_of_blank=round((v - b) / b * 100, 1) if b else np.nan,
            ))
    return pd.DataFrame(rows).sort_values(
        "pct_of_blank", ascending=False, key=abs)


# ---------------------------------------------------------------------------
# Four-parameter logistic dose-response
# ---------------------------------------------------------------------------
def fit_4pl(dose: np.ndarray, resp: np.ndarray):
    """Returns (params, ec50, ec50_ci) or None. params = (bottom, top, ec50, hill)."""
    try:
        from scipy.optimize import curve_fit
    except ImportError:
        return None

    dose, resp = np.asarray(dose, float), np.asarray(resp, float)
    keep = (dose > 0) & np.isfinite(resp)
    if keep.sum() < 5 or len(np.unique(dose[keep])) < 4:
        return None
    x, y = dose[keep], resp[keep]

    def model(xx, bottom, top, ec50, hill):
        return bottom + (top - bottom) / (1 + (xx / ec50) ** hill)

    p0 = [float(np.min(y)), float(np.max(y)), float(np.median(x)), 1.0]
    # Bound ec50 strictly positive: without this the optimiser wanders into
    # negative ec50, where (x/ec50)**hill is a fractional power of a negative
    # number, and numpy emits an invalid-value warning on every such step.
    bounds = ([-np.inf, -np.inf, 1e-9, 1e-3],
              [np.inf, np.inf, float(x.max()) * 1e3, 50.0])
    try:
        popt, pcov = curve_fit(model, x, y, p0=p0, bounds=bounds, maxfev=20000)
    except Exception:                               # noqa: BLE001
        return None
    perr = np.sqrt(np.diag(pcov)) if np.all(np.isfinite(pcov)) else [np.nan] * 4
    ec50, se = popt[2], perr[2]
    ci = (ec50 - 1.96 * se, ec50 + 1.96 * se) if np.isfinite(se) else (np.nan, np.nan)
    return popt, ec50, ci


def dose_response_table(norm: pd.DataFrame) -> pd.DataFrame:
    rows = []
    veh = norm[norm["treatment"] == "vehicle"]
    for (diff, read), g in veh.groupby(["differentiation", "readout"]):
        res = fit_4pl(g["glutamate_mM"].to_numpy(), g["pct_control"].to_numpy())
        if res is None:
            rows.append(dict(differentiation=diff, readout=read,
                             ec50_mM=np.nan, ci_lo=np.nan, ci_hi=np.nan,
                             note="not enough doses, or fit failed"))
            continue
        _, ec50, (lo, hi) = res
        rows.append(dict(differentiation=diff, readout=read,
                         ec50_mM=round(float(ec50), 3),
                         ci_lo=round(float(lo), 3), ci_hi=round(float(hi), 3),
                         note=""))
    return pd.DataFrame(rows)


def ci_overlap(a: tuple[float, float], b: tuple[float, float]) -> bool | None:
    if any(not np.isfinite(v) for v in (*a, *b)):
        return None
    return not (a[1] < b[0] or b[1] < a[0])


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def report(d: pd.DataFrame, path: str, want_dose: bool) -> None:
    bar = "=" * 78
    print(f"\n{bar}\nASSAY MATRIX ANALYSIS  (Proposal A)\nsource: {path}\n{bar}")

    cells = d.loc[~d["cellfree"]]
    print(f"\nwells: {len(d)} total, {len(cells)} with cells, "
          f"{len(d) - len(cells)} cell-free")
    print(f"independent experiments (n): {cells['experiment'].nunique()}")
    print(f"readouts: {', '.join(sorted(cells['readout'].unique()))}")

    agg = aggregate(d)
    norm = normalise_to_vehicle(agg)

    # --- PRIMARY ---------------------------------------------------------
    print(f"\n{bar}\nPRIMARY OUTPUT -- does the answer depend on the readout?\n{bar}")
    dep = readout_dependence(norm)
    if dep.empty:
        print("  (no glutamate-treated, non-vehicle conditions found)")
    else:
        print("\nApparent protection by treatment and readout "
              "(percentage points vs damage control):")
        print(dep.to_string(index=False))

        spread = readout_spread(dep)
        print("\n** THE FIGURE 5 TABLE ** -- spread of the same effect across readouts:")
        print(spread.to_string(index=False))
        if not spread.empty and np.isfinite(spread["spread"].iloc[0]):
            top = spread.iloc[0]
            print(f"\n  Largest readout-dependence: {top['treatment']} in "
                  f"{top['differentiation']} cells varies by "
                  f"{top['spread']} percentage points\n  depending only on "
                  f"which viability assay was used.")

    anova = three_way_anova(norm)
    if anova is not None:
        inter = [i for i in anova.index if ":" in i]
        print("\nANOVA -- interaction terms first (these are the result):")
        if inter:
            print(anova.loc[inter].to_string())
        else:
            print("  (no interaction terms estimable in this design)")
        main = [i for i in anova.index if ":" not in i and i != "Residual"]
        if main:
            print("\n  main effects (secondary):")
            print(anova.loc[main].to_string())

        # Power caveat. An interaction term needs far more n than a main
        # effect, so a non-significant interaction sitting next to a large
        # effect-size spread means "underpowered", not "no effect". Saying so
        # here stops that being misread as a negative result.
        n_exp = cells["experiment"].nunique()
        tr_term = next((i for i in inter
                        if "treatment" in i and "readout" in i), None)
        big_spread = (not dep.empty and not spread.empty
                      and float(spread["spread"].iloc[0]) >= 10)
        if tr_term is not None and big_spread:
            p = float(anova.loc[tr_term, "PR(>F)"])
            if p > 0.05:
                print(f"\n  !! CAUTION: the treatment x readout interaction is "
                      f"not significant (p = {p:.2f}),\n     yet the largest "
                      f"observed readout spread is "
                      f"{spread['spread'].iloc[0]} percentage points at "
                      f"n = {n_exp}.\n     An interaction term needs several "
                      "times the n of a main effect. Do NOT read\n     this as "
                      "'readout does not matter' -- it is an underpowered test "
                      "sitting next\n     to a large descriptive effect. "
                      "Report the effect-size table as the primary\n     "
                      "result, state the interaction was underpowered, and use "
                      "the observed\n     variance to compute the n a "
                      "confirmatory test would need.")

    # --- CELL-FREE -------------------------------------------------------
    print(f"\n{bar}\nCELL-FREE INTERFERENCE -- what the compound does to the dye alone\n{bar}")
    inf = interference(d)
    if inf.empty:
        print("\n  No cell-free wells in this file. This is the cheapest and most\n"
              "  decisive control in the whole proposal -- medium + compound +\n"
              "  dye, no cells. Run it before anything else.")
    else:
        print()
        print(inf.to_string(index=False))
        big = inf[inf["pct_of_blank"].abs() > 10]
        if not big.empty:
            print("\n  ** Compounds altering the dye signal by >10% of blank "
                  "with NO cells present:")
            for _, r in big.iterrows():
                print(f"     {r['treatment']:<12} {r['readout']:<10} "
                      f"{r['pct_of_blank']:+.1f}% of blank")
            print("\n  Any apparent protection by these compounds in the same "
                  "readout is inflated\n  by an amount this table bounds.")
        else:
            print("\n  No compound shifts any dye by >10% of blank. The "
                  "interference axis is weak\n  in this dataset -- report that "
                  "as a negative rather than dropping it.")

    # --- DOSE RESPONSE ---------------------------------------------------
    if want_dose:
        print(f"\n{bar}\nDOSE-RESPONSE (4PL)\n{bar}\n")
        dr = dose_response_table(norm)
        print(dr.to_string(index=False))
        ok = dr[dr["note"] == ""]
        for read, g in ok.groupby("readout"):
            if g["differentiation"].nunique() == 2:
                u = g[g["differentiation"] == "undiff"].iloc[0]
                v = g[g["differentiation"] == "diff"].iloc[0]
                ov = ci_overlap((u["ci_lo"], u["ci_hi"]), (v["ci_lo"], v["ci_hi"]))
                verdict = ("CIs OVERLAP -> differentiation effect not resolved"
                           if ov else "CIs separate -> differentiation effect resolved"
                           if ov is False else "CI not estimable")
                print(f"\n  {read}: undiff EC50 {u['ec50_mM']} vs diff "
                      f"{v['ec50_mM']} mM -- {verdict}")

    print(f"\n{bar}")
    print("Reminder: the claim this analysis supports is about THIS cell line "
          "under THESE\nconditions. Effect sizes and CIs above are reportable; "
          "p-values alone are not.\nNo conclusion here licenses a statement "
          "about neurons in vivo.")
    print(f"{bar}\n")

    dest = os.path.join(os.path.dirname(os.path.abspath(path)) or ".",
                        "assay_matrix_normalised.csv")
    norm.to_csv(dest, index=False)
    print(f"Normalised per-experiment data written to: {dest}\n")


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
def make_fake(seed: int = 7) -> pd.DataFrame:
    """Simulate a dataset with a KNOWN readout-dependent artifact.

    Ground truth built in:
      - glutamate kills ~60% of cells, both differentiation states
      - MK801 genuinely protects ~25 points, but only in differentiated cells
      - DTT genuinely protects ~10 points in undifferentiated cells
      - DTT ADDITIONALLY inflates every reduction-based dye by ~15 points
        with no cells present (the artifact we want the script to surface)
    """
    rng = np.random.default_rng(seed)
    rows = []
    readouts = ["CCK8", "MTT", "resazurin", "LDH"]
    treatments = ["vehicle", "MK801", "DTT"]
    true_prot = {("diff", "MK801"): 25.0, ("undiff", "MK801"): 2.0,
                 ("diff", "DTT"): 3.0, ("undiff", "DTT"): 10.0}
    dye_art = {"CCK8": 15.0, "MTT": 18.0, "resazurin": 6.0, "LDH": 0.0}

    for exp in [f"exp{i}" for i in range(1, 5)]:
        for diff, treat, read in itertools.product(
                ["undiff", "diff"], treatments, readouts):
            for glut in (0.0, 5.0):
                base = 100.0
                if glut > 0:
                    base -= 60.0
                    base += true_prot.get((diff, treat), 0.0)
                    if treat != "vehicle":
                        base += dye_art[read] if read in REDUCTION_READOUTS else 0.0
                for w in range(3):                 # technical wells
                    rows.append(dict(
                        experiment=exp, plate=f"p_{exp}_{read}",
                        well=f"{diff[0].upper()}{w+1}",
                        differentiation=diff, treatment=treat,
                        glutamate_mM=glut, readout=read,
                        raw_value=max(rng.normal(base, 6.0), 0.1) / 100.0,
                        cellfree="FALSE"))
    # dose-response arm (vehicle only, several doses)
    for exp in [f"exp{i}" for i in range(1, 5)]:
        for diff, read in itertools.product(["undiff", "diff"], readouts):
            ec50 = 1.0 if diff == "diff" else 8.0
            for glut in (0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0):
                resp = 100.0 / (1 + (glut / ec50) ** 1.6)
                for w in range(2):
                    rows.append(dict(
                        experiment=exp, plate=f"dr_{exp}_{read}",
                        well=f"D{w+1}", differentiation=diff,
                        treatment="vehicle", glutamate_mM=glut, readout=read,
                        raw_value=max(rng.normal(resp, 5.0), 0.1) / 100.0,
                        cellfree="FALSE"))
    # cell-free arm
    for exp in [f"exp{i}" for i in range(1, 5)]:
        for treat, read in itertools.product(treatments, readouts):
            base = 0.08 + (dye_art[read] / 100.0 if treat == "DTT"
                           and read in REDUCTION_READOUTS else 0.0)
            for w in range(3):
                rows.append(dict(
                    experiment=exp, plate=f"cf_{exp}", well=f"F{w+1}",
                    differentiation="undiff", treatment=treat,
                    glutamate_mM=0.0, readout=read,
                    raw_value=max(rng.normal(base, 0.01), 0.001),
                    cellfree="TRUE"))
    return pd.DataFrame(rows)


def selftest() -> int:
    d = coerce_types(make_fake())
    checks: list[tuple[str, bool]] = []

    missing = [c for c in REQUIRED_COLS if c not in d.columns]
    checks.append(("simulated data has every required column", not missing))

    check_replication(d)
    checks.append(("accepts data with 4 independent experiments", True))

    one = d[d["experiment"] == "exp1"]
    try:
        check_replication(one)
        checks.append(("rejects single-experiment data", False))
    except SystemExit:
        checks.append(("rejects single-experiment data", True))

    norm = normalise_to_vehicle(aggregate(d))
    checks.append(("normalisation produces ~100 for untreated controls",
                   abs(norm[(norm["treatment"] == "vehicle")
                            & (norm["glutamate_mM"] == 0)]["pct_control"]
                       .mean() - 100) < 1.0))

    inf = interference(d)
    dtt = inf[(inf["treatment"] == "DTT")]
    checks.append(("cell-free arm flags the planted DTT dye artifact",
                   bool((dtt[dtt["readout"].isin(REDUCTION_READOUTS)]
                         ["pct_of_blank"] > 50).all())))
    checks.append(("cell-free arm leaves LDH clean",
                   bool(abs(dtt[dtt["readout"] == "LDH"]
                            ["pct_of_blank"].iloc[0]) < 20)))

    dep = readout_dependence(norm)
    spread = readout_spread(dep)
    dtt_un = spread[(spread["treatment"] == "DTT")
                    & (spread["differentiation"] == "undiff")]
    checks.append(("recovers readout-dependence for the artifact compound",
                   bool(len(dtt_un) and dtt_un["spread"].iloc[0] > 8)))
    checks.append(("reduction-minus-orthogonal is positive for DTT",
                   bool(len(dtt_un)
                        and dtt_un["reduction_minus_orthogonal"].iloc[0] > 5)))

    mk_diff = dep[(dep["treatment"] == "MK801")
                  & (dep["differentiation"] == "diff")
                  & (dep["readout"] == "LDH")]
    checks.append(("recovers true MK801 protection in diff cells (LDH)",
                   bool(len(mk_diff)
                        and mk_diff["apparent_protection"].iloc[0] > 15)))

    g, lo, hi = hedges_g(np.array([10, 11, 12, 13.]), np.array([1, 2, 3, 4.]))
    checks.append(("Hedges' g positive with non-overlapping CI",
                   bool(g > 2 and lo > 0)))
    checks.append(("Hedges' g returns nan for n<2",
                   bool(np.isnan(hedges_g(np.array([1.]), np.array([2.]))[0]))))

    fit = fit_4pl(np.array([0.25, .5, 1, 2, 4, 8, 16.]),
                  np.array([98, 95, 80, 50, 22, 8, 3.]))
    checks.append(("4PL fit recovers EC50 near 2",
                   bool(fit is not None and 1.0 < fit[1] < 3.5)))

    dr = dose_response_table(norm)
    ok = dr[dr["note"] == ""]
    checks.append(("dose-response table fits both differentiation states",
                   bool(ok["differentiation"].nunique() == 2)))

    anova = three_way_anova(norm)
    checks.append(("ANOVA yields at least one interaction term",
                   bool(anova is not None
                        and any(":" in i for i in anova.index))))

    for name, ok_ in checks:
        print(f"  [{'PASS' if ok_ else 'FAIL'}] {name}")
    failed = [n for n, o in checks if not o]
    print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
    if failed:
        print("failed: " + "; ".join(failed))
    return 1 if failed else 0


# ---------------------------------------------------------------------------
def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", nargs="?", help="long-format well-level CSV")
    ap.add_argument("--selftest", action="store_true",
                    help="run built-in checks on simulated data and exit")
    ap.add_argument("--dose-response", action="store_true",
                    help="also fit 4PL dose-response curves")
    ap.add_argument("--demo", action="store_true",
                    help="run the full report on simulated data")
    a = ap.parse_args(argv[1:])

    if a.selftest:
        return selftest()
    if a.demo:
        tmp = "._demo_assay_matrix.csv"
        make_fake().to_csv(tmp, index=False)
        try:
            d = load(tmp)
            check_replication(d)
            report(d, tmp, want_dose=True)
        finally:
            for f in (tmp, "assay_matrix_normalised.csv"):
                if os.path.exists(f):
                    os.remove(f)
        return 0
    if not a.csv:
        ap.print_help()
        return 2
    if not os.path.exists(a.csv):
        raise SystemExit(f"File not found: {a.csv}")

    d = load(a.csv)
    check_replication(d)
    report(d, a.csv, want_dose=a.dose_response)
    return 0


if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("always")
        sys.exit(main(sys.argv))
