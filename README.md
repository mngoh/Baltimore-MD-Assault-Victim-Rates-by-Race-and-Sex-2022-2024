# Assault victims in Baltimore

Who gets assaulted in Baltimore, as rates rather than counts: victims of common and aggravated assault reported by the Baltimore Police Department, 2022 to 2024, by race and sex, against ACS population. It is the Baltimore companion to the Los Angeles ([LA-Crime](https://github.com/mngoh/LA-Crime)) and DC (DC-Assault) analyses and uses the same method, packaged as [disparity-kit](https://github.com/mngoh/disparity-kit). It is the first city started from a name with the kit's `/new-city` skill.

The full page is `index.html`.

## Results

Every number below is generated from `out/results.json`, `out/baltimore_checks.json` and `out/replication.json`.

<!-- results:start -->
**Black women in Baltimore are assaulted at about 2.5 to 3 times the rate of White women, and age, police district and neighborhood do not explain it. How they compare with Hispanic women cannot be settled: ethnicity is unknown for 42% of women victims.**

Rates per 100,000 residents a year, 2022-01-01 to 2024-12-31:

| Group | Women | Men |
|---|---|---|
| Black | 3,605 | 3,218 |
| Hispanic | 2,229 | 2,515 |
| White | 1,397 | 1,606 |
| Asian | 641 | 1,599 |

Tests:

- Age: standardized, Black women 3,752 vs 2,154 Hispanic, 1,301 White, 369 Asian.
- Location: 1,664 expected vs 3,605 actual; 1 to 5.1 times inside every rated police district.
- Type: aggravated assault 2 times Hispanic, 3 times White, 6.7 times Asian; common assault 1.5 times Hispanic, 2.4 times White, 5.2 times Asian.
- Time: 3,611, 3,690, 3,513.
- Premises: Other/Residential 62.0% vs 56.0%, Street 22.1% vs 23.7%, School 3.4% vs 1.6% (Black women vs other women).
- Weapons: Firearm 7.6% vs 4.7%, Knife or cutting 4.2% vs 3.6%, Blunt object or vehicle 5.0% vs 5.6%, Hands, fists, feet 73.9% vs 76.8%, Other or unknown 9.4% vs 9.2% (Black women vs other women).

| Controls | Black women vs other women |
|---|---|
| group only | 2.62x |
| + age | 3.03x |
| + year | 3.03x |
| + district | 3.52x |
| + tract socioeconomics | 2.84x |

Pairwise, fully adjusted: Hispanic 2.9x, White 3.09x, Asian 17.85x.

Replication: Hispanic 1.62x then 1.59x; White 2.58x then 2.87x; Asian 5.62x then 7.81x.

Caveats:

- This shows what, not why: The data says Black women are assaulted at a higher rate. It does not say why. Nothing here measures causes, offenders or circumstances.
- Reported crimes only: Every number is a report that reached the police. Willingness to report, and recording practice, differ by group, area and time.
- Reports, not people: Rates count reports. Someone assaulted twice counts twice, so a rate is not the share of people assaulted.
- Exposure is not population: Rates divide by where people live, not where they spend time.
- Who is recorded as Black: Race is recorded by officers; the population counts people who are Black alone. There are 5% more people who are Black alone or in combination. If multiracial victims are recorded as Black, the worst case is 1.54x Hispanic, 2.46x White, 5.35x Asian instead of 1.62x, 2.58x, 5.62x.
- Overlapping groups: 1.2% of Black residents are also Hispanic, so they sit in both denominators.
- Who is counted: 2,093 victims are left out of the rates: their sex is unknown, or their race is unknown or outside the compared groups. Race is unknown or outside the groups for 2.3% of women and 5.4% of men.
- Policing and reporting: Police data reflects where officers patrol and who calls them. This data cannot separate more policing or more reporting from more assaults.
- Hispanic ethnicity is often missing: Baltimore records ethnicity apart from race, and began recording it in June 2021. It is unknown or blank for 41.6% of women victims. 41.9% of women recorded as White have unknown ethnicity, and where it is known, 18.1% of them are Hispanic. They are counted as White here. If they were Hispanic, Black women's rate would be 0.82x Hispanic women's instead of 1.62x, and 4.85x White women's instead of 2.58x. 934 women with unknown race but Hispanic ethnicity are counted as Hispanic.
- Missing race: 523 women victims (2.0%) have unknown race. It is most common in the Southern district (3.0%) and least in the Western district (1.2%), and it is more common where fewer Black women live (correlation -0.76 across districts). That understates other groups' rates slightly, which widens the gap. Spread over the four groups like known victims of the same assault type in the same district, the ratios move to 1.61x Hispanic, 2.57x White, 5.61x Asian from 1.62x, 2.58x, 5.62x.
- Districts are placed by location: Baltimore redrew its police districts in 2023, and the data names the old district before mid-2023 and the new one after. Here every assault is placed in the 2023 district that holds its coordinates, for all three years, so one map is used throughout. 99.9% of victims are placed; 65 have no usable coordinates.
- Neighborhood is not neutral: Police district and tract poverty, income, unemployment and housing are shaped by segregation and disinvestment. Here the adjusted gap (2.84x) is wider than the crude one (2.62x), so these controls do not account for it. Where a control narrows a gap, the gap has been located, not explained away.
- Intimate partner assault cannot be separated: No code or field marks assaults by a partner, so the partner test from the Los Angeles and DC analyses cannot run. In both, partner assault was close to half of assaults on women.
- Officers are not separated: The data does not record the victim type, so assaults on police officers are counted with everyone else's. Los Angeles and DC left them out.
- What is counted: Common assault (code 4E) and aggravated assault (codes 4A, 4B, 4C, 4D, 9S, 3), which includes 1,739 non-fatal shootings Baltimore codes apart from aggravated assault. Homicides are left out. 148 American Indian or Alaska Native victims and 76 Native Hawaiian or Pacific Islander victims are counted in the totals but not compared, because counts this small give unstable rates. 396 women victims with unknown age fall out of the age test only. When an assault has several victims, each is counted.
- Window and population: Victims cover January 2022 to December 2024: full years with ethnicity recorded, before Baltimore police moved to NIBRS in January 2025. The population is the ACS 2024 5-year estimate, an average over 2020 to 2024.
- Least stable comparison: The Asian comparison moved +39% between the legacy system (2022 to 2024) and NIBRS (January 2025 to August 2026) (+54% for aggravated assault), against 11% or less for the others. It rests on 151 Asian women victims in 2022 to 2024 and 59 Asian women victims in January 2025 to August 2026, so it is left out of the headline.
<!-- results:end -->

## How this differs from Los Angeles and DC

- **Source.** The Baltimore Police Department's own open data on Open Baltimore (ArcGIS), the legacy Part 1 file. Its columns carry no descriptions; the data dictionary in the dataset's description says Race, Gender, Age and Ethnicity are the victim's.
- **Location, as in LA.** Coordinates are recorded for almost every victim, so the district test and the tract-level model run. DC's NIBRS files had no location.
- **Districts are placed by location.** Baltimore redrew its police districts in 2023, and the data names the old district before mid-2023 and the new one after. Every assault is placed in the 2023 district that holds its coordinates, so one map covers all three years.
- **Race and ethnicity are separate fields, as in DC.** A victim is Hispanic if the ethnicity field says so, whatever the race, and otherwise takes the recorded race. Baltimore began recording ethnicity in June 2021 and it is often missing, so the Hispanic comparison carries a wide range (see the caveats) and stays out of the headline.
- **No partner or victim-type field.** The partner test cannot run, and assaults on officers cannot be left out.
- **Shootings are coded apart.** Baltimore codes non-fatal shootings separately from aggravated assault. They are counted as aggravated assault, as NIBRS and LA count them.
- **Replication, as in LA.** Baltimore moved to NIBRS in January 2025, so the second source is a different records system: the NIBRS file from 2025 on.

## Definitions

- Offenses: common assault (4E) and aggravated assault (4A to 4D: firearm, cutting instrument, other weapon, hands) plus non-fatal shootings (9S, and the rows coded 4A or 3 that are labeled SHOOTING). Homicides are left out.
- Agency: Baltimore Police Department. Victims: every recorded victim. The data has no victim type, so officers are included.
- Window: January 2022 to December 2024. These are full years with ethnicity recorded, before the move to NIBRS. The audit found no coverage breaks inside them.
- Groups: Black, Hispanic, White and Asian, as recorded by officers. Unknown race, sex and ethnicity stay unknown. Nothing is imputed; the district comes from each record's own coordinates.
- Times: the portal labels its timestamps UTC, but the hour pattern (fewest assaults at 5 to 6 a.m.) shows local times. They are used as recorded.

## Rebuild

Python from disparity-kit (`~/.claude/disparity-kit/.venv/bin/python`); `KIT=~/.claude/disparity-kit/kit`. Needs the kit's new-city scripts (`sources.py`, `schema.py`, `prepare.py` with `--district-from`).

```bash
# data (the raw files are not tracked: the legacy file is over GitHub's size limit)
python $KIT/sources.py fetch "https://services1.arcgis.com/UWYHeuuJISiGmgXx/arcgis/rest/services/Part1_Crime_Beta/FeatureServer/0" --out data/raw/bpd_part1_legacy.csv
python $KIT/sources.py fetch "https://services1.arcgis.com/UWYHeuuJISiGmgXx/arcgis/rest/services/NIBRS_GroupA_Crime_Data/FeatureServer/0" --out data/raw/bpd_nibrs_groupa.csv
python $KIT/audit.py data/raw/bpd_part1_legacy.csv --date CrimeDateTime --code CrimeCode --desc Description --id CCNumber --out out/audit_legacy.md
python $KIT/audit.py data/raw/bpd_nibrs_groupa.csv --date CrimeDateTime --code CrimeCode --desc Description --id CCNumber --out out/audit_nibrs.md

# mapping (analysis.draft.json, then analysis.json with the decisions)
python $KIT/schema.py map data/raw/bpd_part1_legacy.csv --source out/source_part1.json --out out/mapping.json
python $KIT/schema.py districts data/raw/bpd_part1_legacy.csv --mapping out/mapping.json --geojson "https://services1.arcgis.com/UWYHeuuJISiGmgXx/arcgis/rest/services/Police_Districts_New/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=geojson" --out out/districts.json
python $KIT/schema.py place "Baltimore, MD" --out out/place.json
python $KIT/schema.py draft --mapping out/mapping.json --districts out/districts.json --place out/place.json --source out/source_part1.json --out analysis.draft.json

# analysis files, one per type
python $KIT/prepare.py data/raw/bpd_part1_legacy.csv --code CrimeCode --kind simple=4E --kind aggravated=4A,4B,4C,4D,9S,3 --out-dir data --prefix bpd_ \
  --hispanic-first --race Race --ethnicity Ethnicity --hispanic HISPANIC_OR_LATINO --race-out race_group \
  --district-from out/districts.json --lat Latitude --lon Longitude

python $KIT/denominators.py analysis.json            # -> out/population.json
python $KIT/analyze.py analysis.json                 # -> out/results.json
python scripts/replication_counts.py analysis.json   # -> out/replication_counts.json
python $KIT/replicate.py analysis.json               # -> out/replication.json
python scripts/baltimore_checks.py analysis.json     # -> out/baltimore_checks.json, extra_caveats in analysis.json
python $KIT/build_page.py analysis.json              # -> index.html, results block above
python $KIT/bias_scan.py analysis.json               # -> out/bias_review.md
```

## Files

- `data/raw/*.csv.source.json`: where each raw file came from (url, time, rows). The raw CSVs are refetched with the commands above.
- `data/bpd_simple.csv`, `data/bpd_aggravated.csv`: the analysis input, one row per victim, all years, every raw column plus `race_group` and `district_geo`. `data/prepare.json` records the rule.
- `analysis.draft.json`: the config as `/new-city` drafted it, before the decisions. `analysis.json` is the one the kit runs.
- `out/`: the source inspections, audits, mapping, district match, population, results, Baltimore checks, replication and bias review.

## Sources

- Baltimore Police Department, [Part 1 Crime Data (Legacy SRS)](https://www.arcgis.com/home/item.html?id=e0992dddbbf64231976d5d57763ec4f5) and [NIBRS Group A Crime Data](https://www.arcgis.com/home/item.html?id=204beefe92a645d79fdf0969957bbdf8), Open Baltimore.
- Baltimore City police districts, 2023 boundaries, Open Baltimore.
- US Census Bureau, ACS 2020 to 2024 five-year estimates, via [Census Reporter](https://censusreporter.org/profiles/16000US2404000-baltimore-md/).
