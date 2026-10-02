"""Counts for the replication check: the legacy records system (the analysis window) against NIBRS.

Baltimore police moved to NIBRS on January 1, 2025. The legacy file (Part 1, SRS) stops there, and the NIBRS
Group A file carries the new system. Same women, same race rule, same population; only the records system and
the years differ.

  primary     legacy SRS, 2022 to 2024: the analysis's own files (data/bpd_simple.csv, data/bpd_aggravated.csv)
  secondary   NIBRS, January 2025 to August 2026: data/raw/bpd_nibrs_groupa.csv. September 2026 is left out
              because the latest weeks are still filling in (reporting lag).

Matching: 13B simple assault for 4E common assault; 13A aggravated assault for 4A to 4D plus shootings (NIBRS has
no separate shooting code; shootings are 13A). Neither file records victim type, so officers are counted in both.
NIBRS rows are one per victim per offense: a victim listed under both 13A and 13B in one case (same case number,
sex, age, race and ethnicity) is counted once in "all", as aggravated.

  python scripts/replication_counts.py analysis.json   ->  out/replication_counts.json
  then: python ~/.claude/disparity-kit/kit/replicate.py analysis.json
"""
import json
import pathlib
import sys

import numpy as np
import pandas as pd

NIBRS = "data/raw/bpd_nibrs_groupa.csv"
NIBRS_KIND = {"13B": "simple", "13A": "aggravated"}
NIBRS_SPAN = ("2025-01-01", "2026-08-31")
HISPANIC = "HISPANIC_OR_LATINO"


def years(a, b):
    a, b = pd.Timestamp(a), pd.Timestamp(b)
    return round(sum(((min(b, pd.Timestamp(y, 12, 31)) - max(a, pd.Timestamp(y, 1, 1))).days + 1) / (366 if y % 4 == 0 else 365)
                     for y in range(a.year, b.year + 1)), 4)


def counts(d, groups):
    cats = {"all": d}
    cats.update({k: d[d["kind"] == k] for k in ("simple", "aggravated")})
    return {c: {g: int((x["group"] == g).sum()) for g in groups} for c, x in cats.items()}


def main():
    cfg_path = pathlib.Path(sys.argv[1]).resolve()
    root = cfg_path.parent
    cfg = json.loads(cfg_path.read_text())
    S, groups, rm = cfg["focus"].get("sex", "F"), cfg["groups"], cfg["race_map"]
    col = cfg["columns"]
    w0, w1 = cfg["window"]["start"], cfg["window"]["end"]

    old = pd.concat([pd.read_csv(root / s["path"], dtype=str, keep_default_na=False).assign(kind=s["kind"]) for s in cfg["incidents"]])
    old = old[(old[col["date"]].str[:10] >= w0) & (old[col["date"]].str[:10] <= w1) & (old[col["sex"]] == S)]
    old["group"] = old[col["race"]].map(rm)

    new = pd.read_csv(root / NIBRS, dtype=str, keep_default_na=False)
    new = new[new["CrimeCode"].isin(NIBRS_KIND) & (new["CrimeDateTime"].str[:10] >= NIBRS_SPAN[0]) & (new["CrimeDateTime"].str[:10] <= NIBRS_SPAN[1])].copy()
    new["kind"] = new["CrimeCode"].map(NIBRS_KIND)
    new["group"] = pd.Series(np.where(new["Ethnicity"] == HISPANIC, "H", new["Race"]), index=new.index).map(rm)
    new = new[new["Gender"] == S]
    person = ["CCNumber", "Gender", "Age", "Race", "Ethnicity"]
    both = new.sort_values("kind").duplicated(person, keep="first") & new.groupby(person)["kind"].transform("nunique").gt(1)
    new_all = new[~both]

    sources = {"primary": {"label": f"Legacy system, {w0[:4]} to {w1[:4]}", "years": years(w0, w1), "counts": counts(old, groups)},
               "secondary": {"label": "NIBRS, January 2025 to August 2026", "years": years(*NIBRS_SPAN), "counts": counts(new, groups)}}
    sources["secondary"]["counts"]["all"] = counts(new_all, groups)["all"]
    spec = {"sources": sources,
            "definition_notes": "Legacy SRS 2022 to 2024 against NIBRS January 2025 to August 2026 (September 2026 left out for reporting lag). "
                                "13B simple assault matched to 4E common assault; 13A aggravated assault to 4A to 4D plus shootings. "
                                "Women victims, Hispanic of any race first by the ethnicity column, otherwise the recorded race, in both. "
                                f"A woman listed under both 13A and 13B in one case is counted once in the total, as aggravated ({int(both.sum())} in this period). "
                                "Neither file records victim type, so assaults on officers are in both."}
    out = root / "out" / "replication_counts.json"
    out.write_text(json.dumps(spec, indent=1))
    print("wrote", out)
    for k, s in sources.items():
        print(k, s["label"], s["years"], s["counts"]["all"])


if __name__ == "__main__":
    main()
