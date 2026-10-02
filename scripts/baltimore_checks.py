"""Baltimore-specific checks the kit does not run, and the caveats they produce.

  ethnicity bound   the legacy file records ethnicity apart from race, from June 2021, and it is often missing.
                    White-race women with unknown ethnicity are counted as White; here they are moved to Hispanic, or
                    split in the known proportion, to bound the Hispanic and White comparisons.
  missing race      women victims with unknown race are spread over the four groups in proportion to known victims of
                    the same assault type in the same police district, and the ratios recomputed. Also: where unknown
                    race is most common, against the Black share of women residents in each district.
  districts         how many victims the coordinates place in a district (the 2023 map, for every year)
  counted           what is in and out: codes, groups not compared, unknown age

Writes out/baltimore_checks.json and regenerates `extra_caveats` in analysis.json from it, so every number in
the caveats comes from this output.

  python scripts/baltimore_checks.py analysis.json
"""
import json
import os
import re
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.expanduser(os.environ.get("DISPARITY_KIT", "~/.claude/disparity-kit/kit")))
from common import Project, load_incidents, year_spans  # noqa: E402

UNKNOWN_ETH = {"", "UNKNOWN"}
NOT_COMPARED = {"AMERICAN_INDIAN_OR_ALASKA_NATIVE": "American Indian or Alaska Native", "NATIVE_HAWAIIAN_OR_OTHER_PACIFIC_ISLANDER": "Native Hawaiian or Pacific Islander"}


def ratio(a, b):
    return round(a / b, 2) if b else None


def main():
    p = Project(sys.argv[1])
    G, S = p.focus
    pop = p.read_json("population.json")
    city = pop["city"]
    R = p.read_json("results.json")
    _, years = year_spans(p)
    rate = lambda n, g: round(n / city[g][S] / years * 1e5)  # rounded like the kit, so "as mapped" matches results.json
    df = load_incidents(p)
    raw = pd.concat([pd.read_csv(p.path(s["path"]), dtype=str, keep_default_na=False).assign(kind=s["kind"]) for s in p.cfg["incidents"]])
    start, end = p.window()
    raw = raw[(raw["CrimeDateTime"].str[:10] >= f"{start:%Y-%m-%d}") & (raw["CrimeDateTime"].str[:10] <= f"{end:%Y-%m-%d}")]
    women = raw[raw["Gender"] == S]
    groups = p.groups
    code_of = {g: [k for k, v in p.cfg["race_map"].items() if v == g] for g in groups}
    out = {}

    # ethnicity bound
    w = women[(women["Race"] == "WHITE") & (women["race_group"] == "WHITE")]
    w_unknown = int(w["Ethnicity"].isin(UNKNOWN_ETH).sum())
    white_all = women[women["Race"] == "WHITE"]
    w_known_h = int((white_all["Ethnicity"] == "HISPANIC_OR_LATINO").sum())
    w_known_n = int((~white_all["Ethnicity"].isin(UNKNOWN_ETH | {"HISPANIC_OR_LATINO"})).sum())
    share_h = w_known_h / (w_known_h + w_known_n)
    n = {g: int(women["race_group"].isin(code_of[g]).sum()) for g in groups}
    scen = {"as mapped": (n["Hispanic"], n["White"]),
            "unknown ethnicity left out": (n["Hispanic"], n["White"] - w_unknown),
            "split in known proportion": (n["Hispanic"] + share_h * w_unknown, n["White"] - share_h * w_unknown),
            "all Hispanic": (n["Hispanic"] + w_unknown, n["White"] - w_unknown)}
    fr = rate(n[G], G)
    out["ethnicity"] = {
        "white_race_women": len(white_all), "white_unknown_ethnicity": w_unknown, "white_unknown_pct": round(w_unknown / len(white_all) * 100, 1),
        "hispanic_share_where_known_pct": round(share_h * 100, 1),
        "all_unknown_ethnicity_pct": round(float(women["Ethnicity"].isin(UNKNOWN_ETH).mean() * 100), 1),
        "hispanic_recovered_from_unknown_race": int(((women["Race"].isin({"", "UNKNOWN"})) & (women["Ethnicity"] == "HISPANIC_OR_LATINO")).sum()),
        "scenarios": {k: {"Hispanic": ratio(fr, rate(h, "Hispanic")), "White": ratio(fr, rate(wh, "White"))} for k, (h, wh) in scen.items()},
    }
    sc = out["ethnicity"]["scenarios"]
    assert sc["as mapped"]["Hispanic"] == R["ratios"]["Hispanic"] and sc["as mapped"]["White"] == R["ratios"]["White"], "counts differ from results.json"
    out["ethnicity"]["hispanic_range"] = [min(v["Hispanic"] for v in sc.values()), max(v["Hispanic"] for v in sc.values())]
    out["ethnicity"]["white_range"] = [min(v["White"] for v in sc.values()), max(v["White"] for v in sc.values())]

    # missing race: redistributed inside type x district, and where it clusters
    fs = df[df["sex"] == S].copy()
    fs["unknown"] = fs["race"].isna() & ~fs["race_raw"].isin(NOT_COMPARED)
    fs["cell"] = fs["kind"] + "|" + fs["district"].fillna("none").astype(str)
    counts = {g: 0.0 for g in groups}
    for _, c in fs.groupby("cell"):
        known = c["race"].value_counts()
        tot = sum(known.get(g, 0) for g in groups)
        for g in groups:
            counts[g] += known.get(g, 0) + (c["unknown"].sum() * known.get(g, 0) / tot if tot else 0)
    rr = {g: rate(counts[g], g) for g in groups}
    by_d = fs.groupby("district")["unknown"].mean().mul(100).round(1)
    black_share = {d: round(c[G][S] / sum(c[g][S] for g in groups) * 100, 1) for d, c in pop["districts"].items()}
    corr = float(np.corrcoef([by_d[d] for d in by_d.index], [black_share[d] for d in by_d.index])[0, 1])
    out["missing_race"] = {
        "unknown_women": int(fs["unknown"].sum()), "unknown_pct": round(float(fs["unknown"].mean() * 100), 1),
        "unknown_pct_by_district": by_d.to_dict(), "black_share_of_women_by_district": black_share,
        "correlation_with_black_share": round(corr, 2),
        "ratios_redistributed": {g: ratio(rr[G], rr[g]) for g in p.others}, "ratios_as_mapped": R["ratios"],
    }

    # districts placed by location
    prep = json.loads((p.root / "data" / "prepare.json").read_text())
    out["districts"] = {"placed_pct": round(float(df["district"].notna().mean() * 100), 1), "unplaced": int(df["district"].isna().sum()),
                        "boundaries": prep["district_rule"]["boundaries"].get("geojson_url")}

    # what is counted
    kinds = json.loads((p.root / "data" / "prepare.json").read_text())["kinds"]
    out["counted"] = {
        "codes": kinds, "victims": len(df), "women": int((df["sex"] == S).sum()),
        "by_kind": df["kind"].value_counts().to_dict(),
        "shootings": int(df["code"].isin(["9S", "3"]).sum() + ((raw["CrimeCode"] == "4A") & (raw["Description"] == "SHOOTING")).sum()),
        "not_compared": {label: int((raw["race_group"] == code).sum()) for code, label in NOT_COMPARED.items()},
        "age_unknown": int(fs["age"].isna().sum()),
        "sex_unknown": int(df["sex"].isna().sum()),
    }
    p.write_json("baltimore_checks.json", out)

    # caveats, generated from the checks above
    e, m, d, x = out["ethnicity"], out["missing_race"], out["districts"], out["counted"]
    release = pop["release"]
    acs_year = int(re.search(r"\d{4}", release).group())
    hi = max(m["unknown_pct_by_district"], key=m["unknown_pct_by_district"].get)
    lo = min(m["unknown_pct_by_district"], key=m["unknown_pct_by_district"].get)
    caveats = [
        ["Policing and reporting",
         "Police data reflects where officers patrol and who calls them. This data cannot separate more policing or more reporting from more assaults."],
        ["Hispanic ethnicity is often missing",
         f"Baltimore records ethnicity apart from race, and began recording it in June 2021. It is unknown or blank for {e['all_unknown_ethnicity_pct']}% of women victims. "
         f"{e['white_unknown_pct']}% of women recorded as White have unknown ethnicity, and where it is known, {e['hispanic_share_where_known_pct']}% of them are Hispanic. "
         f"They are counted as White here. If they were Hispanic, Black women's rate would be {e['hispanic_range'][0]}x Hispanic women's instead of {R['ratios']['Hispanic']}x, "
         f"and {e['white_range'][1]}x White women's instead of {R['ratios']['White']}x. "
         f"{e['hispanic_recovered_from_unknown_race']:,} women with unknown race but Hispanic ethnicity are counted as Hispanic."],
        ["Missing race",
         f"{m['unknown_women']:,} women victims ({m['unknown_pct']}%) have unknown race. It is most common in the {hi.title()} district ({m['unknown_pct_by_district'][hi]}%) "
         f"and least in the {lo.title()} district ({m['unknown_pct_by_district'][lo]}%), and it is more common where fewer Black women live "
         f"(correlation {m['correlation_with_black_share']} across districts). That understates other groups' rates slightly, which widens the gap. "
         f"Spread over the four groups like known victims of the same assault type in the same district, "
         f"the ratios move to " + ", ".join(f"{m['ratios_redistributed'][g]}x {g}" for g in p.others) + " from " + ", ".join(f"{R['ratios'][g]}x" for g in p.others) + "."],
        ["Districts are placed by location",
         f"Baltimore redrew its police districts in 2023, and the data names the old district before mid-2023 and the new one after. Here every assault is placed in the 2023 "
         f"district that holds its coordinates, for all three years, so one map is used throughout. {d['placed_pct']}% of victims are placed; {d['unplaced']:,} have no usable coordinates."],
        ["Neighborhood is not neutral",
         f"Police district and tract poverty, income, unemployment and housing are shaped by segregation and disinvestment. Here the adjusted gap "
         f"({R['model']['ladder'][-1]['rate_ratio']}x) is wider than the crude one ({R['model']['ladder'][0]['rate_ratio']}x), so these controls do not account for it. "
         "Where a control narrows a gap, the gap has been located, not explained away."],
        ["Intimate partner assault cannot be separated",
         "No code or field marks assaults by a partner, so the partner test from the Los Angeles and DC analyses cannot run. In both, partner assault was close to half of assaults on women."],
        ["Officers are not separated",
         "The data does not record the victim type, so assaults on police officers are counted with everyone else's. Los Angeles and DC left them out."],
        ["What is counted",
         f"Common assault (code {', '.join(x['codes']['simple'])}) and aggravated assault (codes {', '.join(x['codes']['aggravated'])}), which includes "
         f"{x['shootings']:,} non-fatal shootings Baltimore codes apart from aggravated assault. Homicides are left out. "
         + " and ".join(f"{v} {k} victims" for k, v in x["not_compared"].items()) + " are counted in the totals but not compared, because counts this small give unstable rates. "
         f"{x['age_unknown']:,} women victims with unknown age fall out of the age test only. When an assault has several victims, each is counted."],
        ["Window and population",
         f"Victims cover {start:%B %Y} to {end:%B %Y}: full years with ethnicity recorded, before Baltimore police moved to NIBRS in January 2025. "
         f"The population is the {release} estimate, an average over {acs_year - 4} to {acs_year}."],
    ]
    rep_path = p.out / "replication.json"
    if rep_path.exists():
        rep = json.loads(rep_path.read_text())
        allc = rep["comparison"]["all"]
        worst = max(allc, key=lambda g: abs(allc[g]["change_pct"]))
        rest = max(abs(allc[g]["change_pct"]) for g in allc if g != worst)
        biggest = max(((c, v[worst]["change_pct"]) for c, v in rep["comparison"].items() if worst in v), key=lambda t: abs(t[1]))
        labels = [src["label"] for src in rep["sources"].values()]
        n_small = {src["label"]: src["counts"]["all"][worst] for src in json.loads((p.out / "replication_counts.json").read_text())["sources"].values()}
        out["least_stable"] = {"group": worst, "change_pct": allc[worst]["change_pct"], "others_max_pct": rest, "largest": biggest, "victims": n_small}
        p.write_json("baltimore_checks.json", out)
        caveats.append(["Least stable comparison",
                        f"The {worst} comparison moved {allc[worst]['change_pct']:+d}% between the legacy system ({labels[0].split(', ')[-1]}) and NIBRS ({labels[1].split(', ')[-1]}) "
                        f"({biggest[1]:+d}% for {p.cfg.get('kind_labels', {}).get(biggest[0], biggest[0]).lower()}), against {rest}% or less for the others. "
                        f"It rests on " + " and ".join(f"{v:,} {worst} women victims in {k.split(', ')[-1]}" for k, v in n_small.items()) + ", so it is left out of the headline."])
    cfg = json.loads(p.config_path.read_text())
    cfg["extra_caveats"] = caveats
    p.config_path.write_text(json.dumps(cfg, indent=1, ensure_ascii=False) + "\n")
    print("updated extra_caveats in", p.config_path.name)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
