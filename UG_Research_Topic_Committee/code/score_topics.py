#!/usr/bin/env python3
"""
score_topics.py -- Transparent, reproducible scoring of candidate research
topics for an undergraduate original-research project.

This is a direct port of score_topics.R. It exists because R was not available
in the environment where these deliverables were prepared, so the scoring
reported in 02_15_Candidate_Topics.md was actually produced and checked with
this file. Both scripts read the same CSV and apply the same rubric; they
should give the same answer, and `--selftest` checks the arithmetic.

WHY THIS SCRIPT EXISTS
    A 100-point rubric is easy to apply dishonestly: pick the favourite, then
    back-fill the sub-scores. This forces the opposite order. Sub-scores live
    in a flat CSV, weights live in one place, and the ranking is computed.

    It keeps four DIFFERENT success measures separate, because conflating them
    is the most common planning error in undergraduate projects:
        p_exec   = P(experiments can physically be completed)
        p_paper  = P(results, whatever they are, assemble into a paper)
        p_accept = P(that paper is accepted by an SCI-indexed journal)
        sci_val  = scientific value -- NOT a probability, never multiplied in

    Every number is an elicited judgement, not a measurement. They are recorded
    so they can be argued with, not so they can be believed.

USAGE
    python3 score_topics.py [path/to/topic_scores.csv]
    python3 score_topics.py --selftest

DEPENDENCIES
    pandas. (Standard library only would also work, but pandas is already a
    prerequisite for the rest of the student's analysis work.)
"""

from __future__ import annotations

import os
import sys

import pandas as pd

# ---- 1. The rubric ----------------------------------------------------------
# Weights are the committee's, and must sum to 100.
WEIGHTS: dict[str, int] = {
    "importance":      15,  # Significance of the scientific question
    "novelty":         20,  # Genuine novelty (not the 6 pseudo-novelty traps)
    "fit_resources":   15,  # Fit to the student's ACTUAL platform
    "operability":     15,  # Can the experiments really be run, by this person
    "finish_6_12mo":   10,  # Probability of finishing in 6-12 months
    "sci_potential":   15,  # SCI publication potential (NOT impact factor)
    "negative_value":   5,  # Scientific value of the negative result
    "ug_contribution":  5,  # Room for independent undergraduate contribution
}
assert sum(WEIGHTS.values()) == 100, "rubric weights must sum to 100"

SCORE_MAX = 10          # each dimension is scored 0-10 in the CSV
PROB_COLS = ["p_exec", "p_paper", "p_accept"]
HML_COLS = ["novelty_rating", "evidence_rating", "overlap_risk"]


def required_columns() -> list[str]:
    return (["id", "short_name"] + list(WEIGHTS)
            + PROB_COLS + HML_COLS + ["confidence"])


# ---- 2. Validate ------------------------------------------------------------
def validate(d: pd.DataFrame) -> None:
    """Fail loudly on bad input rather than silently producing a ranking."""
    missing = [c for c in required_columns() if c not in d.columns]
    if missing:
        raise SystemExit(f"Missing required column(s): {', '.join(missing)}")

    if d["id"].duplicated().any():
        dups = d.loc[d["id"].duplicated(), "id"].tolist()
        raise SystemExit(f"Duplicate topic id(s): {dups}")

    for nm in WEIGHTS:
        col = pd.to_numeric(d[nm], errors="coerce")
        bad = d.loc[col.isna() | (col < 0) | (col > SCORE_MAX), "id"].tolist()
        if bad:
            raise SystemExit(
                f"Column '{nm}' must be 0-{SCORE_MAX}; bad row(s): {bad}")

    for nm in PROB_COLS:
        col = pd.to_numeric(d[nm], errors="coerce")
        bad = d.loc[col.isna() | (col < 0) | (col > 1), "id"].tolist()
        if bad:
            raise SystemExit(
                f"Column '{nm}' must be a probability in [0,1]; bad row(s): {bad}")

    for nm in HML_COLS:
        bad = d.loc[~d[nm].astype(str).str.upper().isin(["H", "M", "L"]),
                    "id"].tolist()
        if bad:
            raise SystemExit(f"Column '{nm}' must be H/M/L; bad row(s): {bad}")


# ---- 3. Score ---------------------------------------------------------------
def score(d: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    d = d.copy()
    weighted = pd.DataFrame(
        {nm: pd.to_numeric(d[nm]) / SCORE_MAX * w for nm, w in WEIGHTS.items()},
        index=d.index,
    )
    d["total"] = weighted.sum(axis=1).round(1)

    # Composite pipeline probability: chance this ends as an accepted paper.
    # Deliberately a product -- the three stages are sequential gates, so the
    # product is always smaller than any single stage. That is the honest result.
    d["p_published"] = (pd.to_numeric(d["p_exec"])
                        * pd.to_numeric(d["p_paper"])
                        * pd.to_numeric(d["p_accept"])).round(3)

    # A topic can score well on the rubric and still be a bad bet, or score
    # modestly and be a good bet. Flag the divergence instead of hiding it.
    d["rubric_rank"] = d["total"].rank(ascending=False, method="min").astype(int)
    d["pipeline_rank"] = d["p_published"].rank(ascending=False,
                                               method="min").astype(int)
    d["rank_divergence"] = d["pipeline_rank"] - d["rubric_rank"]

    # Blocking flags: things that should stop a topic regardless of total score.
    up = lambda c: d[c].astype(str).str.upper()
    flags = [
        up("overlap_risk").eq("H").map({True: "HIGH-OVERLAP", False: ""}),
        up("evidence_rating").eq("L").map({True: "THIN-EVIDENCE", False: ""}),
        d["confidence"].astype(str).str.lower().eq("low")
            .map({True: "LOW-CONFIDENCE", False: ""}),
    ]
    d["flags"] = (flags[0] + " " + flags[1] + " " + flags[2]).str.replace(
        r"\s+", " ", regex=True).str.strip()
    return d, weighted


# ---- 4. Report --------------------------------------------------------------
def report(d: pd.DataFrame, weighted: pd.DataFrame, csv_path: str) -> None:
    bar = "=" * 78
    print(f"\n{bar}\nCANDIDATE TOPIC SCORING\nsource: {csv_path}\n{bar}\n")

    print("Rubric weights (sum = 100):")
    for nm, w in WEIGHTS.items():
        print(f"  {nm:<16} {w:>3}")
    print()

    d = d.sort_values("total", ascending=False)
    cols = ["id", "short_name", "total"] + PROB_COLS + [
        "p_published", "novelty_rating", "overlap_risk", "flags"]
    out = d[cols].rename(columns={
        "id": "ID", "short_name": "Topic", "total": "Score",
        "p_exec": "pExec", "p_paper": "pPaper", "p_accept": "pAccept",
        "p_published": "pPub", "novelty_rating": "Nov",
        "overlap_risk": "Ovl", "flags": "Flags"})
    print(out.to_string(index=False))

    print("\n-- Dimension detail (weighted points) --")
    det = weighted.loc[d.index].round(1)
    det.insert(0, "id", d["id"].values)
    print(det.to_string(index=False))

    print("\n-- Rank divergence (pipeline rank minus rubric rank) --")
    print("   Positive = scores better on the rubric than its odds justify.")
    print("   Negative = a better bet than its rubric score suggests.\n")
    div = d.reindex(d["rank_divergence"].abs().sort_values(
        ascending=False).index)
    print(div[["id", "short_name", "rubric_rank", "pipeline_rank",
               "rank_divergence"]].head(10).to_string(index=False))

    print("\n-- Topics carrying a blocking flag --")
    fl = d.loc[d["flags"] != "", ["id", "short_name", "total", "flags"]]
    print("   none" if fl.empty else fl.to_string(index=False))

    print("\nNOTE: every number above is an elicited judgement, not a "
          "measurement.\n      p_published is a product of three subjective "
          "probabilities and is\n      therefore the least reliable figure in "
          "the table. Use it to compare\n      topics against each other, "
          "never as a forecast of success.\n")

    dest = os.path.join(os.path.dirname(os.path.abspath(csv_path)),
                        "topic_scores_ranked.csv")
    d.to_csv(dest, index=False)
    print(f"Ranked table written to: {dest}\n")


# ---- 5. Self-test -----------------------------------------------------------
def selftest() -> int:
    """Check the arithmetic on a hand-computable case."""
    row_full = {nm: SCORE_MAX for nm in WEIGHTS}
    row_half = {nm: SCORE_MAX / 2 for nm in WEIGHTS}
    base = dict(p_exec=0.5, p_paper=0.5, p_accept=0.5, novelty_rating="H",
                evidence_rating="H", overlap_risk="L", confidence="medium")
    d = pd.DataFrame([
        {"id": "T1", "short_name": "all tens", **row_full, **base},
        {"id": "T2", "short_name": "all fives", **row_half, **base},
    ])
    validate(d)
    scored, _ = score(d)
    t1 = scored.loc[scored["id"] == "T1"].iloc[0]
    t2 = scored.loc[scored["id"] == "T2"].iloc[0]
    checks = [
        ("all-tens scores 100", t1["total"] == 100.0),
        ("all-fives scores 50", t2["total"] == 50.0),
        ("p_published is the product", t1["p_published"] == 0.125),
        ("product < each factor", t1["p_published"] < 0.5),
        ("rubric rank assigned", t1["rubric_rank"] == 1),
        ("no spurious flags", t1["flags"] == ""),
    ]
    bad_input = d.copy()
    bad_input.loc[0, "novelty"] = 99
    try:
        validate(bad_input)
        checks.append(("out-of-range rejected", False))
    except SystemExit:
        checks.append(("out-of-range rejected", True))

    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    failed = [n for n, ok in checks if not ok]
    print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
    return 1 if failed else 0


# ---- 6. Entry point ---------------------------------------------------------
def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()

    here = os.path.dirname(os.path.abspath(__file__))
    default_csv = os.path.join(here, "..", "data", "topic_scores.csv")
    csv_path = argv[1] if len(argv) > 1 else default_csv

    if not os.path.exists(csv_path):
        raise SystemExit(
            f"Score file not found: {csv_path}\n"
            "Create it with the columns listed in this script's header, or "
            "pass a path as the first argument.")

    d = pd.read_csv(csv_path)
    validate(d)
    scored, weighted = score(d)
    report(scored, weighted, os.path.abspath(csv_path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
