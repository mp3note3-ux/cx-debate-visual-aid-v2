# CX Debate Visual Aids

Python-generated, 16:9 presentation visuals for the CEDA/CX debate on whether local governments should operate selected public libraries as overnight heat shelters during heatwaves.

## Repository contents

- Seven 1920×1080 PNG visual aids in `visuals/`
- Seven-page combined PDF: `debate_heat_visual_aids.pdf`
- Contact-sheet preview: `contact_sheet.png`
- Reproducible Python source: `make_visuals.py`
- Published aggregate data tables and source notes in `data/`
- GitHub Actions workflow that rebuilds and commits the outputs when source files change

## Visuals

| # | File | Debate placement |
|---|---|---|
| 01 | [KDCA: home occurrence and older adults](visuals/01_KDCA_home_and_older_adults.png) | First speaker — accessibility |
| 02 | [GeoHealth forest plot](visuals/02_GeoHealth_forest_plot.png) | First speaker — compound heatwaves |
| 03 | [Seoul library hours timeline](visuals/03_Seoul_library_hours_timeline.png) | First speaker — operating hours |
| 04 | [Seoul targeted heat protection](visuals/04_Seoul_targeted_protection_dashboard.png) | Second speaker — existing measures |
| 05 | [Cooling-centre evidence gap](visuals/05_Dearman_evidence_gap.png) | Second speaker — quality of evidence |
| 06 | [Accessibility chain](visuals/06_Accessibility_chain.png) | First speaker — conceptual framework |
| 07 | [Three-question team summary](visuals/07_Three_question_summary.png) | Shared closing visual |

Preview: [contact_sheet.png](contact_sheet.png)  
Combined presentation: [debate_heat_visual_aids.pdf](debate_heat_visual_aids.pdf)

## Rebuild locally

Use Python 3.10 or newer:

```bash
pip install -r requirements.txt
python make_visuals.py
```

The script reads the CSV inputs already stored in `data/` and regenerates the seven PNGs, PDF and contact sheet.

## Data and interpretation cautions

- KDCA tables are published aggregate surveillance counts, not patient-level raw data. The surveillance system uses participating emergency departments and is not a census.
- The 65+ age subtotal overlaps the individual age bands. Place-of-occurrence parent totals overlap their subgroups. Do not add those overlapping rows.
- GeoHealth CSV values are published adjusted odds ratios and confidence intervals, not the underlying NHIS admissions dataset. The study's underlying data require NHIS approval.
- The nighttime-only GeoHealth estimate is not statistically significant; the compound daytime-and-nighttime estimate is statistically significant. Do not conflate them.
- The Seoul 2025 programme's KRW 10.6 billion figure refers to the broader extended-hours programme, not a dedicated overnight heat-shelter budget.
- The Dearman review's absence of real-world cooling-centre health-outcome studies is an evidence gap, not proof that cooling centres are ineffective.
- The accessibility chain and final summary are conceptual presentation frameworks, not measured datasets.

See [data/README.md](data/README.md) for full source descriptions and limitations.

## Sources

- KDCA, 「올해 온열질환자 8.8% 감소했지만 추정 사망자는 증가, 고령층 보호 강화 필요」, 2026-10-12: https://www.kdca.go.kr/bbs/kdca/42/310219/download.do
- Kim et al. (2026), *GeoHealth*, 10(10), e2026GH001920: https://doi.org/10.1029/2026GH001920
- Seoul Metropolitan Government (2025), public-library extended-hours programme: https://english.seoul.go.kr/122-seoul-public-libraries-extend-hours-to-10-pm-transforming-into-climate-shelters/
- 서울특별시 (2026), 「서울시, 여름철 무더위로부터 거리 노숙인·쪽방주민 보호에 만전」: https://www.seoul.go.kr/news/news_report.do?nttNo=459300
- Dearman et al. (2025), *Oxford Open Climate Change*, 5(1), kgaf020: https://doi.org/10.1093/oxfclm/kgaf020
- Lee & Han (2024), *Urban Climate*, 55, 101869: https://doi.org/10.1016/j.uclim.2024.101869

## Design

The chart style uses a restrained government-report palette: navy, steel blue, neutral greys, off-white, and one brick-red accent. All chart elements are drawn with Python; no AI-generated images or external decorative assets are used.
