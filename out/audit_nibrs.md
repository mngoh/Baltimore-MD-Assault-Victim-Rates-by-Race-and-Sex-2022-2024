# Audit: data/raw/bpd_nibrs_groupa.csv

274,697 rows, 24 columns. Guessed: date `CrimeDateTime`, code `CrimeCode`, description `Description`, id `CCNumber`. Override with flags if wrong.

## Missing and coded-missing values

| column | blank | coded missing (0, X, UNKNOWN...) | distinct |
|---|---|---|---|
| RowID | 0.0% | 0.0% | 274,697 |
| CCNumber | 0.0% | 0.0% | 237,422 |
| CrimeDateTime | 0.0% | 0.0% | 160,886 |
| CrimeCode | 0.0% | 0.0% | 43 |
| Description | 0.0% | 0.0% | 28 |
| Inside_Outside | 0.1% | 0.0% | 2 |
| Weapon | 63.9% | 0.5% | 21 |
| Shooting | 99.2% | 0.0% | 2 |
| Post | 0.1% | 0.0% | 203 |
| Gender | 14.9% | 0.4% | 3 |
| Age | 16.6% | 0.1% | 105 |
| Race | 22.8% | 1.8% | 6 |
| Ethnicity | 8.3% | 42.3% | 7 |
| Location | 0.6% | 0.0% | 15,383 |
| Old_District | 67.0% | 0.0% | 9 |
| New_District | 30.7% | 0.0% | 10 |
| Neighborhood | 20.1% | 0.0% | 290 |
| Latitude | 0.1% | 0.0% | 67,044 |
| Longitude | 0.1% | 0.0% | 77,557 |
| GeoLocation | 0.0% | 0.0% | 106,546 |
| PremiseType | 0.0% | 1.0% | 39 |
| Total_Incidents | 0.0% | 0.0% | 1 |
| lon | 0.1% | 0.0% | 77,557 |
| lat | 0.1% | 0.0% | 67,044 |

## Duplicates

37,275 rows share an id in `CCNumber`. One row per victim or offense? Decide before counting.

## Every offense value

Read the whole list. Related offenses are often coded separately (intimate partner, on police, on children, attempts).

| CrimeCode | Description | rows |
|---|---|---|
| 13B | COMMON ASSAULT | 45,899 |
| 290 | VANDALISM | 41,282 |
| 240 | AUTO THEFT | 29,045 |
| 13A | AGG. ASSAULT | 26,361 |
| 23F | LARCENY FROM AUTO | 20,079 |
| 23H | LARCENY | 19,241 |
| 220 | BURGLARY | 16,295 |
| 23C | SHOPLIFTING | 15,487 |
| 120 | ROBBERY | 13,414 |
| 23G | LARCENY OF MOTOR VEHICLE PARTS OR ACCESSORIES | 10,118 |
| 23D | LARCENY | 7,296 |
| 13C | INTIMIDATION | 6,745 |
| 26A | FRAUD | 3,808 |
| 26D | FRAUD | 2,525 |
| 26B | FRAUD | 2,362 |
| 120 | ROBBERY - COMMERCIAL | 2,355 |
| 120 | ROBBERY - CARJACKING | 2,252 |
| 26F | FRAUD | 1,512 |
| 26E | FRAUD | 1,253 |
| 11A | RAPE | 1,058 |
| 250 | FRAUD | 1,055 |
| 09A | HOMICIDE | 985 |
| 11D | SEX OFFENSES | 879 |
| 200 | ARSON | 590 |
| 280 | STOLEN PROPERTY | 524 |
| 11B | RAPE | 351 |
| 100 | KIDNAPPING | 300 |
| 23B | LARCENY | 247 |
| 270 | FRAUD | 210 |
| 210 | EXTORTION | 195 |
| 370 | PORNOGRAPHY | 165 |
| 23A | LARCENY | 162 |
| 26C | FRAUD | 129 |
| 11C | RAPE | 122 |
| 520 | WEAPON VIOLATIONS | 97 |
| 26G | FRAUD | 81 |
| 64A | HUMAN TRAFFICKING | 44 |
| 23E | LARCENY | 43 |
| 36B | SEX OFFENSES | 43 |
| 720 | ANIMAL CRUELTY | 36 |
| 35A | DRUG/NARCOTIC VIOLATIONS | 36 |
| 64B | HUMAN TRAFFICKING | 9 |
| 36A | SEX OFFENSES | 3 |
| 40C | PROSTITUTION | 2 |
| 35B | DRUG VIOLOATION | 2 |

## Coverage by month

0 unparseable dates. Range 2022-01-01 to 2026-09-28.

Median 4,806 rows a month. Months under 60% of that (system changes, partial periods, reporting lag):

- none

Full series:

2022-01:3745 2022-02:3301 2022-03:3991 2022-04:4138 2022-05:4449 2022-06:4863 2022-07:5028 2022-08:4877 2022-09:4899 2022-10:4991 2022-11:4783 2022-12:4674 2023-01:4546 2023-02:4684 2023-03:5027 2023-04:5018 2023-05:6078 2023-06:5940 2023-07:6816 2023-08:6651 2023-09:6358 2023-10:6471 2023-11:4922 2023-12:5099 2024-01:4711 2024-02:4530 2024-03:4849 2024-04:4629 2024-05:4901 2024-06:5066 2024-07:5282 2024-08:5063 2024-09:5221 2024-10:4955 2024-11:4509 2024-12:4337 2025-01:3934 2025-02:3711 2025-03:4496 2025-04:4520 2025-05:4806 2025-06:4708 2025-07:4843 2025-08:4679 2025-09:4829 2025-10:4731 2025-11:4378 2025-12:4228 2026-01:3894 2026-02:3502 2026-03:4588 2026-04:4783 2026-05:4938 2026-06:5053 2026-07:5069 2026-08:5098 2026-09:4507

Use only full calendar years where you can; weight any partial year by its share of the year.