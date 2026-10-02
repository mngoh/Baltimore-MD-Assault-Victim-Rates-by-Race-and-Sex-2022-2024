# Racial bias review

Focus: Black women. This screen finds candidates; read every flag in context before acting.

## Data

- **note: race coding.** Officers record race by sight; the denominator is Black alone. Alone or in combination is 5% larger. Worst-case ratios: Hispanic 1.54x (from 1.62x), White 2.46x (from 2.58x), Asian 5.35x (from 5.62x). The writeup must state this bound.
- **note: overlapping denominators.** Share of each race-alone group that is also Hispanic: {'Black': 1.2, 'Asian': 1.4}. These residents count in two denominators; small shares are tolerable, large ones need non-Hispanic tables.
- **note: race outside the groups.** 4.3% of victims map to no group. Largest raw codes: `AMERICAN_INDIAN_OR_ALASKA_NATIVE` 148, `UNKNOWN` 147, `NATIVE_HAWAIIAN_OR_OTHER_PACIFIC_ISLANDER` 76. Check none of them should belong to a group.
- **FLAG: where race is missing.** Across 9 districts, correlation between the share of victims with unknown race and the focus group's share of residents: -0.67. Missing race is concentrated where the focus group is scarce, so other groups' rates are likely understated, widening the gap.
- **note: unknown race by sex.** Women 2.3%, men 5.4%.
- **FLAG: unstable comparisons.** Ratios moved more than 25% between sources for: Asian. Do not headline those comparisons; say they are less stable.
- **note: small groups.** Under 50,000 residents of the focus sex: Hispanic, Asian. Their rates carry more noise.
- **note: enforcement and reporting.** Police data reflects where police patrol and who calls them. Heavier policing or more reporting in some neighborhoods raises recorded rates there. The writeup must say the data cannot separate this from real differences.
- **note: controls are not neutral.** Neighborhood, income and housing are shaped by segregation and discrimination. A gap that shrinks after these controls has been located, not explained away; say so.

## Writeup

Files: `index.html`, `README.md`

### index.html
- **review: Causal claim** (`causes`): "The data says Black women are assaulted at a higher rate. It does not say why. Nothing here measures causes, offenders or circumstances."  
  The data shows rates, not causes. Keep causal words only in sentences that say a cause is not measured.
- **review: Causal claim** (`because`): "Common assault (code 4E) and aggravated assault (codes 4A, 4B, 4C, 4D, 9S, 3), which includes 1,739 non-fatal shootings Baltimore codes apart from aggravated assault. Homicides are left out. 148 American Indian or Alaska..."  
  The data shows rates, not causes. Keep causal words only in sentences that say a cause is not measured.
- **review: Offender implication** (`offenders`): "Residents are the denominator, so exposure away from home is unmeasured. Reporting behavior is invisible to police data. Nothing here measures offenders or circumstances."  
  Victim data says nothing about who offended. Remove, or state that offenders are not in the data.
- **review: Offender implication** (`offenders`): "The data says Black women are assaulted at a higher rate. It does not say why. Nothing here measures causes, offenders or circumstances."  
  Victim data says nothing about who offended. Remove, or state that offenders are not in the data.
- **review: Share-of-people claim** (`1.2% of Black residents`): "1.2% of Black residents are also Hispanic, so they sit in both denominators."  
  Report rates count reports, not people. Do not convert them into shares of a population.
- **review: Explained-away language** (`accounts for the gap`): "Women only (20,233 Black women, 4,876 other women). Each cut asks whether a plain explanation accounts for the gap."  
  Controls like neighborhood and income are themselves shaped by segregation and discrimination. 'Explained by location' does not mean 'not related to race'.
- **review: Explained-away language** (`explained away`): "Police district and tract poverty, income, unemployment and housing are shaped by segregation and disinvestment. Here the adjusted gap (2.84x) is wider than the crude one (2.62x), so these controls do not account for it...."  
  Controls like neighborhood and income are themselves shaped by segregation and discrimination. 'Explained by location' does not mean 'not related to race'.

### README.md
- **FLAG: inconsistent capitalization.** Hispanic 19x vs hispanic 2x. Pick one style (AP capitalizes Black; be consistent for White).
- **review: Causal claim** (`causes`): "- This shows what, not why: The data says Black women are assaulted at a higher rate. It does not say why. Nothing here measures causes, offenders or circumstances."  
  The data shows rates, not causes. Keep causal words only in sentences that say a cause is not measured.
- **review: Causal claim** (`because`): "- What is counted: Common assault (code 4E) and aggravated assault (codes 4A, 4B, 4C, 4D, 9S, 3), which includes 1,739 non-fatal shootings Baltimore codes apart from aggravated assault. Homicides are left out. 148 Americ..."  
  The data shows rates, not causes. Keep causal words only in sentences that say a cause is not measured.
- **review: Offender implication** (`offenders`): "- This shows what, not why: The data says Black women are assaulted at a higher rate. It does not say why. Nothing here measures causes, offenders or circumstances."  
  Victim data says nothing about who offended. Remove, or state that offenders are not in the data.
- **review: Share-of-people claim** (`1.2% of Black residents`): "- Overlapping groups: 1.2% of Black residents are also Hispanic, so they sit in both denominators."  
  Report rates count reports, not people. Do not convert them into shares of a population.
- **review: Explained-away language** (`explained away`): "- Neighborhood is not neutral: Police district and tract poverty, income, unemployment and housing are shaped by segregation and disinvestment. Here the adjusted gap (2.84x) is wider than the crude one (2.62x), so these ..."  
  Controls like neighborhood and income are themselves shaped by segregation and discrimination. 'Explained by location' does not mean 'not related to race'.

### Required statements

- present: says it does not explain why
- present: names reporting differences
- present: names the race-coding limit
- present: separates reports from people

## Reviewer questions (answer in prose, not by regex)

- Does any sentence invite the reader to infer who the offenders are?
- Would the framing read the same if the groups were swapped?
- Is the comparison group chosen to make the gap look larger (for example, headlining the most extreme pair)?
- Are structural explanations (segregation, policing intensity, access to services) acknowledged as unmeasured, without being asserted?
- Does the headline survive the race-coding worst case and the least favorable comparison?
- Is the focus group described with agency and dignity, as people harmed, not as a problem?