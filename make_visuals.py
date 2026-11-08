from pathlib import Path
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "visuals"
OUT.mkdir(exist_ok=True)

# Read numeric source tables from the repository.
kdca = pd.read_csv(DATA / "kdca_2025_2026_comparison.csv")
geo = pd.read_csv(DATA / "geohealth_published_odds_ratios.csv")

# Restrained public-sector palette: dark navy, steel blue, neutrals, one red accent.
BG, WHITE = "#F5F6F4", "#FFFFFF"
NAVY, BLUE, RED = "#18344F", "#486B86", "#A94332"
DARK, MID, GREY = "#18232D", "#5C6872", "#AEB8C0"
LIGHT, GRID = "#E6EAED", "#D9DEE2"

installed = {f.name for f in font_manager.fontManager.ttflist}
FONT = next((f for f in [
    "NanumSquare", "Noto Sans CJK KR", "Noto Sans KR",
    "Malgun Gothic", "AppleGothic"
] if f in installed), "DejaVu Sans")

sns.set_theme(style="whitegrid", context="notebook", font=FONT)
plt.rcParams.update({
    "font.family": FONT,
    "axes.unicode_minus": False,
    "figure.facecolor": BG,
    "axes.facecolor": WHITE,
    "savefig.facecolor": BG,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titleweight": "bold",
})

SIZE, DPI = (13.333, 7.5), 144
generated = []

def header(fig, number, title, subtitle, section):
    fig.text(.065, .945, "DEBATE EVIDENCE  /  DATA VISUAL",
             fontsize=9.5, color=BLUE, weight="bold", va="top")
    fig.text(.065, .895, title, fontsize=22, color=NAVY,
             weight="bold", va="top")
    fig.text(.065, .845, subtitle, fontsize=11, color=MID, va="top")
    fig.text(.93, .93, f"{number:02d}", fontsize=18,
             color=RED, weight="bold", ha="right", va="top")
    fig.text(.935, .845, section, fontsize=9.2, color=MID,
             ha="right", va="top")

def footer(fig, source, note=""):
    if note:
        fig.text(.065, .075, note, fontsize=7.8, color=MID, va="bottom")
    fig.text(.065, .035, source, fontsize=7.0, color=MID, va="bottom")

def card(ax, x, y, w, h):
    p = FancyBboxPatch((x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.025",
        linewidth=1, edgecolor=LIGHT, facecolor=WHITE,
        transform=ax.transAxes, clip_on=False, zorder=1)
    ax.add_patch(p)

def save(fig, name):
    path = OUT / name
    fig.savefig(path, dpi=DPI, bbox_inches=None)
    generated.append(path)
    plt.close(fig)

def value(metric, column):
    return int(kdca.loc[kdca.metric == metric, column].iloc[0])

# ---------------------------------------------------------------------
# 01. KDCA: home occurrence and older adults
# ---------------------------------------------------------------------
h25 = value("At home occurrence", "2025_value")
h26 = value("At home occurrence", "2026_value")
s25 = value("Age 65+", "2025_value")
s26 = value("Age 65+", "2026_value")
t25 = value("All heat-illness cases", "2025_value")
t26 = value("All heat-illness cases", "2026_value")

fig = plt.figure(figsize=SIZE)
header(fig, 1, "전체 신고는 감소했지만, 집에서 발생한 환자는 증가했습니다",
       "질병관리청 온열질환 응급실감시체계 · 2025년과 2026년 비교",
       "FIRST SPEAKER  /  ACCESS")

ax = fig.add_axes([.08, .22, .47, .53])
ax.grid(axis="x", color=GRID)
ax.grid(axis="y", visible=False)
ax.set_axisbelow(True)
bars = ax.bar(["2025년", "2026년"], [h25, h26],
              width=.52, color=[GREY, RED], zorder=3)
ax.set_ylim(0, 430)
ax.set_ylabel("집에서 발생한 온열질환 신고 건수")
ax.set_yticks([0, 100, 200, 300, 400])
ax.set_title("집에서 발생한 온열질환자",
             loc="left", fontsize=14, pad=16)
for b, n in zip(bars, [h25, h26]):
    ax.text(b.get_x()+b.get_width()/2, n+12, f"{n:,}명",
            ha="center", fontsize=15, weight="bold",
            color=RED if n == h26 else DARK)
ax.text(.05, .96, f"+{(h26/h25-1)*100:.1f}%",
        transform=ax.transAxes, ha="left", va="top",
        fontsize=23, weight="bold", color=RED)
ax.text(.05, .86, "전년 대비", transform=ax.transAxes,
        ha="left", va="top", fontsize=9.5, color=MID)

ax2 = fig.add_axes([.62, .20, .31, .57])
ax2.axis("off")
card(ax2, 0, .60, 1, .36)
ax2.text(.08, .89, "65세 이상 온열질환자",
         transform=ax2.transAxes, fontsize=11, color=MID, va="top")
ax2.text(.08, .73, f"{s26:,}명", transform=ax2.transAxes,
         fontsize=26, color=NAVY, weight="bold", va="top")
ax2.text(.08, .64,
         f"2025년 {s25:,}명 → 2026년 {s26:,}명  (+{(s26/s25-1)*100:.1f}%)",
         transform=ax2.transAxes, fontsize=9.0, color=MID, va="top")
card(ax2, 0, .18, 1, .34)
ax2.text(.08, .44, "전체 신고환자 중 65세 이상 비중",
         transform=ax2.transAxes, fontsize=10, color=MID, va="top")
ax2.text(.08, .29, f"{s26/t26*100:.1f}%",
         transform=ax2.transAxes, fontsize=25, color=RED,
         weight="bold", va="top")
ax2.text(.08, .06,
         f"전체 신고환자: {t25:,}명 → {t26:,}명 ({(t26/t25-1)*100:.1f}%)",
         transform=ax2.transAxes, fontsize=8.9, color=MID, va="top")
footer(fig,
       "출처: 질병관리청, 「올해 온열질환자 8.8% 감소했지만 추정 사망자는 증가, 고령층 보호 강화 필요」, 2026.10.12.",
       "주의: 약 520개 참여 응급실 기반 감시자료이며 전수조사가 아닙니다. 신고 온열질환자 수에는 추정 사망자가 포함됩니다.")
save(fig, "01_KDCA_home_and_older_adults.png")

# ---------------------------------------------------------------------
# 02. GeoHealth forest plot
# ---------------------------------------------------------------------
labels = {
    "Daytime heatwave only": "낮 폭염만",
    "Nighttime heatwave only": "밤 폭염만",
    "Compound daytime_and_nighttime heatwave": "낮·밤 복합 폭염",
}
geo["label_kr"] = geo["exposure_type"].map(labels)
geo = geo.set_index("label_kr").loc[
    ["낮 폭염만", "밤 폭염만", "낮·밤 복합 폭염"]
].reset_index()

fig = plt.figure(figsize=SIZE)
header(fig, 2, "낮과 밤의 더위가 함께 이어질 때 응급입원 교차비가 더 높았습니다",
       "전국 응급입원 2,010,769건 분석 · 2011–2019년 6–9월",
       "FIRST SPEAKER  /  OVERNIGHT EFFECT")

ax = fig.add_axes([.13, .23, .48, .50])
ax.set_axisbelow(True)
ax.grid(axis="x", color=GRID)
ax.grid(axis="y", visible=False)

for i, row in geo.iterrows():
    label = row["label_kr"]
    color = RED if label == "낮·밤 복합 폭염" else (
        BLUE if label == "낮 폭염만" else GREY)
    est = float(row["odds_ratio"])
    lo = float(row["ci95_lower"])
    hi = float(row["ci95_upper"])
    ax.errorbar(est, 2-i,
        xerr=[[est-lo], [hi-est]],
        fmt="D" if label == "낮·밤 복합 폭염" else "o",
        color=color, ecolor=color, markersize=9,
        elinewidth=3, capsize=7, capthick=2, zorder=4)

ax.axvline(1.00, color=MID, linewidth=1.4,
           linestyle=(0, (4, 3)), zorder=1)
ax.text(1.002, 2.43, "기준선 1.00",
        fontsize=9, color=MID, ha="left", va="bottom")
ax.set_yticks([2, 1, 0])
ax.set_yticklabels(geo["label_kr"], fontsize=12, weight="bold")
ax.set_xlim(.97, 1.095)
ax.set_ylim(-.55, 2.55)
ax.set_xlabel("교차비 (OR) · 95% 신뢰구간",
              fontsize=10, labelpad=11)
ax.set_xticks([.98, 1.00, 1.02, 1.04, 1.06, 1.08])

right = fig.add_axes([.66, .23, .28, .50])
right.set_xlim(0, 1)
right.set_ylim(-.55, 2.55)
right.axis("off")
right.text(.02, 2.43, "추정치 [95% CI]",
           fontsize=9, color=MID, weight="bold", va="bottom")
for i, row in geo.iterrows():
    y = 2-i
    label = row["label_kr"]
    color = RED if label == "낮·밤 복합 폭염" else (
        BLUE if label == "낮 폭염만" else MID)
    status = ("통계적으로 유의" if
              row["significance_as_reported"] == "statistically_significant"
              else "유의하지 않음")
    right.text(.02, y,
        f'{row["odds_ratio"]:.2f} [{row["ci95_lower"]:.2f}–{row["ci95_upper"]:.2f}]',
        fontsize=10.7, color=color, weight="bold", va="center")
    right.text(.02, y-.23, status,
        fontsize=8.5, color=MID, va="center")

footer(fig,
       "출처: Kim et al., “Compound Heatwaves and Health Inequality…,” GeoHealth, 10(10), 2026, e2026GH001920. DOI: 10.1029/2026GH001920.",
       "주의: OR은 응급입원과의 통계적 관련성입니다. 밤 폭염만의 OR 1.00 (0.98–1.02)은 유의하지 않았으며, 연구는 도서관·쉼터의 효과를 직접 측정하지 않았습니다.")
save(fig, "02_GeoHealth_forest_plot.png")

# ---------------------------------------------------------------------
# 03. Seoul library programme: a single documented 22:00 endpoint
# ---------------------------------------------------------------------
fig = plt.figure(figsize=SIZE)
header(fig, 3, "연장 운영 사업은 도서관 122곳을 오후 10시까지 운영했습니다",
       "서울시 2025년 공공도서관 연장 운영 사업 · 발표된 운영시간 범위",
       "FIRST SPEAKER  /  OPERATING HOURS")

cards_ax = fig.add_axes([.07, .62, .86, .16])
cards_ax.axis("off")
for i, (big, small) in enumerate([
    ("122개관", "연장 운영 도서관"),
    ("378명", "야간 운영 인력"),
    ("106억 원", "연장 운영 사업 전체 예산*")
]):
    x = i * .34
    card(cards_ax, x, .05, .30, .88)
    cards_ax.text(x+.04, .67, big,
        transform=cards_ax.transAxes, fontsize=21,
        color=NAVY, weight="bold", va="top")
    cards_ax.text(x+.04, .28, small,
        transform=cards_ax.transAxes, fontsize=9.5,
        color=MID, va="top")

ax = fig.add_axes([.09, .25, .82, .26])
ax.set_xlim(18, 30)
ax.set_ylim(-.35, 1.05)
ax.set_yticks([])
ax.set_xticks([18, 22, 24, 26, 28, 30])
ax.set_xticklabels(["18:00", "22:00", "00:00", "02:00", "04:00", "06:00"])
ax.grid(axis="x", color=GRID)
ax.grid(axis="y", visible=False)
ax.axvline(22, color=RED, linewidth=3, zorder=3)
ax.scatter([22], [.36], s=150, color=RED, zorder=4)
ax.text(22, .73, "22:00", color=RED, fontsize=19,
        weight="bold", ha="center", va="bottom")
ax.text(22, .58, "사업에서 발표한 운영 종료 시각",
        color=RED, fontsize=9.5, ha="center", va="bottom")
ax.text(26, .35, "이후 심야 운영시간은\n이 사업 발표에서 확인되지 않음",
        color=MID, fontsize=11, ha="center", va="center",
        bbox=dict(boxstyle="round,pad=.6", facecolor=BG,
                  edgecolor=LIGHT, linewidth=1))
ax.set_xlabel("시간 (다음 날 06:00까지)", labelpad=10)
footer(fig,
       "출처: Seoul Metropolitan Government, “122 Seoul Public Libraries Extend Hours to 10 PM, Transforming into Climate Shelters,” 2025.02.24.",
       "* 106억 원은 연장 운영 사업 전체 예산이지, 새벽까지 운영하는 야간 무더위 쉼터 전용 예산이 아닙니다. 이 도표는 해당 사업 발표만 설명합니다.")
save(fig, "03_Seoul_library_hours_timeline.png")

# ---------------------------------------------------------------------
# 04. Seoul targeted protection measures
# ---------------------------------------------------------------------
fig = plt.figure(figsize=SIZE)
header(fig, 4, "서울시는 취약계층별로 서로 다른 폭염 보호수단을 운영하고 있습니다",
       "2026년 서울시 거리 노숙인·쪽방주민 특별보호 대책",
       "SECOND SPEAKER  /  EXISTING MEASURES")

ax = fig.add_axes([.065, .17, .87, .63])
ax.axis("off")

protection = [
    (.00, .53, .31, .39, "11곳", "노숙인 무더위쉼터",
     "24시간 운영으로 발표\n여성전용 시설은 별도 운영시간", NAVY),
    (.345, .53, .31, .39, "8곳", "쪽방주민 무더위쉼터",
     "평일 상시 운영\n7–8월 주말·공휴일 확대", BLUE),
    (.69, .53, .31, .39, "6곳", "쪽방주민 밤더위대피소",
     "7–8월 매일 운영\n6·9·10월 폭염특보 시", RED),
    (.17, .05, .31, .39, "209대", "쪽방촌 공용 에어컨",
     "여름철 전기요금 지원\n필터 청소 지원", BLUE),
    (.515, .05, .31, .39, "141명", "특별보호대상 주민",
     "간호사 방문 건강 확인\n노약자·만성질환자 등", NAVY),
]

for x, y, w, h, big, label, detail, color in protection:
    card(ax, x, y, w, h)
    ax.add_patch(Rectangle((x, y), .012, h,
        transform=ax.transAxes, facecolor=color,
        edgecolor="none", zorder=2))
    ax.text(x+.04, y+h-.06, big, transform=ax.transAxes,
        fontsize=24, color=color, weight="bold", va="top")
    ax.text(x+.04, y+h-.18, label, transform=ax.transAxes,
        fontsize=10.8, color=NAVY, weight="bold", va="top")
    ax.text(x+.04, y+.08, detail, transform=ax.transAxes,
        fontsize=8.3, color=MID, va="bottom", linespacing=1.5)

footer(fig,
       "출처: 서울특별시, 「서울시, 여름철 무더위로부터 거리 노숙인·쪽방주민 보호에 만전」, 2026.06.08.",
       "주의: 서로 다른 사업 단위(시설·장비·대상자)는 합산할 수 없습니다. 여성전용 시설은 별도 운영시간이 명시되어 있습니다.")
save(fig, "04_Seoul_targeted_protection_dashboard.png")

# ---------------------------------------------------------------------
# 05. Dearman systematic review: evidence gap, not ineffectiveness
# ---------------------------------------------------------------------
fig = plt.figure(figsize=SIZE)
header(fig, 5, "냉방센터의 실제 건강 효과를 측정한 연구는 아직 확인되지 않았습니다",
       "냉방센터 관련 문헌의 체계적 고찰 · 2025년 발표",
       "SECOND SPEAKER  /  EVIDENCE QUALITY")

ax = fig.add_axes([.07, .22, .86, .54])
ax.axis("off")
card(ax, .02, .37, .43, .58)
card(ax, .53, .37, .43, .58)

ax.text(.08, .83, "최종 포함 연구",
    transform=ax.transAxes, fontsize=11, color=MID, va="top")
ax.text(.08, .62, "5개",
    transform=ax.transAxes, fontsize=39, color=NAVY,
    weight="bold", va="top")
ax.text(.08, .43, "체계적 문헌고찰에 포함된 연구",
    transform=ax.transAxes, fontsize=9.5, color=MID, va="top")

ax.text(.59, .83, "실제 이용자 건강 결과를 보고한 연구",
    transform=ax.transAxes, fontsize=10.2, color=MID, va="top")
ax.text(.59, .62, "0개",
    transform=ax.transAxes, fontsize=39, color=RED,
    weight="bold", va="top")
ax.text(.59, .43, "냉방센터 이용자의 실제 건강 결과",
    transform=ax.transAxes, fontsize=9.2, color=MID, va="top")

ax.text(.50, .18,
    "근거가 부족하다는 뜻이지, 냉방센터가 효과 없다는 증명은 아닙니다.",
    transform=ax.transAxes, ha="center", va="center",
    fontsize=11.5, color=RED, weight="bold")

footer(fig,
       "출처: Dearman et al., “Public Health Effectiveness of Cooling Centres during Periods of Adverse Hot Weather: A Systematic Literature Review,” Oxford Open Climate Change, 5(1), 2025, kgaf020.",
       "포함 연구는 북미 연구이며 한국 공공도서관의 효과를 직접 평가한 자료가 아닙니다. 3,718건과 흐름도 단계의 수치 차이가 있어 검색 건수 퍼널은 사용하지 않았습니다.")
save(fig, "05_Dearman_evidence_gap.png")

# ---------------------------------------------------------------------
# 06. Accessibility chain: conceptual team framework
# ---------------------------------------------------------------------
fig = plt.figure(figsize=SIZE)
header(fig, 6, "접근성은 도서관의 수가 아니라 실제 이용 과정에서 결정됩니다",
       "팀의 정책 점검 기준 · 공간적 접근성과 실제 이용 가능성을 구분하는 개념도",
       "FIRST SPEAKER  /  ACCESS FRAMEWORK")

ax = fig.add_axes([.06, .26, .88, .45])
ax.axis("off")

steps = [
    ("01", "위치", "도움이 필요한 사람의\n거주지와 가까운가?"),
    ("02", "이동", "거동이 불편한 사람도\n실제로 갈 수 있는가?"),
    ("03", "이용 조건", "입장·안내·이용 규정이\n이용자에게 적합한가?"),
    ("04", "체류", "더위가 이어지는 시간까지\n안전하게 머물 수 있는가?"),
]
xs = [.015, .265, .515, .765]

for i, (number, title, description) in enumerate(steps):
    x = xs[i]
    card(ax, x, .18, .205, .68)
    ax.text(x+.025, .78, number, transform=ax.transAxes,
        fontsize=10, color=RED, weight="bold", va="top")
    ax.text(x+.025, .62, title, transform=ax.transAxes,
        fontsize=15, color=NAVY, weight="bold", va="top")
    ax.text(x+.025, .43, description, transform=ax.transAxes,
        fontsize=8.8, color=MID, va="top", linespacing=1.6)
    if i < 3:
        ax.add_patch(FancyArrowPatch(
            (x+.211, .51), (x+.245, .51),
            arrowstyle="-|>", mutation_scale=15,
            linewidth=1.4, color=RED, transform=ax.transAxes
        ))

ax.text(.50, .03,
    "네 단계가 이어져야 ‘실질적인 보호’로 연결됩니다.",
    transform=ax.transAxes, ha="center", va="bottom",
    fontsize=13, color=RED, weight="bold")

footer(fig,
       "참고 연구: Lee & Han, “Heat Vulnerability and Spatial Equity of Cooling Center: Planning Implications from the Korean Case,” Urban Climate, 55, 2024, 101869.",
       "이 도표는 팀의 토론용 점검 틀이며, 연구가 네 항목을 동일한 척도로 측정했다는 뜻은 아닙니다.")
save(fig, "06_Accessibility_chain.png")

# ---------------------------------------------------------------------
# 07. Three-question team summary
# ---------------------------------------------------------------------
fig = plt.figure(figsize=SIZE)
header(fig, 7, "도서관 야간 쉼터의 실효성은 세 가지 질문으로 검증해야 합니다",
       "두 입론을 하나의 정책 판단 기준으로 연결",
       "TEAM SUMMARY")

ax = fig.add_axes([.065, .22, .87, .53])
ax.axis("off")

summary = [
    (.01, "갈 수 있는가?", "위치 · 이동 · 실제 접근성", "ACCESS"),
    (.345, "머물 수 있는가?", "운영시간 · 냉방 · 야간 안전", "OPERATION"),
    (.68, "효과가 있는가?", "실제 이용 · 보호 효과 · 운영비", "EFFECTIVENESS"),
]

for x, question, description, tag in summary:
    card(ax, x, .18, .30, .67)
    ax.text(x+.04, .76, tag, transform=ax.transAxes,
        fontsize=8.5, color=RED, weight="bold", va="top")
    ax.text(x+.04, .56, question, transform=ax.transAxes,
        fontsize=17, color=NAVY, weight="bold", va="top")
    ax.text(x+.04, .36, description, transform=ax.transAxes,
        fontsize=9.3, color=MID, va="top")

ax.text(.50, .02, "문을 여는 것과 사람을 지키는 것은 다릅니다.",
    transform=ax.transAxes, fontsize=16, color=RED,
    weight="bold", ha="center", va="bottom")

footer(fig,
       "토론팀 입론 구성: 김호직(접근성·운영시간) / 이윤우(효과·비용 대비 검토).",
       "토론용 요약 도표입니다. 통계 추정치나 별도 연구 결과를 나타내는 자료는 아닙니다.")
save(fig, "07_Three_question_summary.png")

# ---------------------------------------------------------------------
# 8. Combined PDF and contact sheet
# ---------------------------------------------------------------------
pdf_path = ROOT / "debate_heat_visual_aids.pdf"
with PdfPages(pdf_path) as pdf:
    for path in generated:
        img = Image.open(path).convert("RGB")
        fig = plt.figure(figsize=SIZE)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.imshow(img)
        ax.axis("off")
        pdf.savefig(fig, facecolor=BG)
        plt.close(fig)

thumbs = []
for path in generated:
    img = Image.open(path).convert("RGB")
    img.thumbnail((640, 360))
    canvas = Image.new("RGB", (660, 390), BG)
    canvas.paste(img, ((660-img.width)//2, 8))
    ImageDraw.Draw(canvas).text(
        (16, 370), path.stem.replace("_", " "), fill=DARK
    )
    thumbs.append(canvas)

cols = 2
rows = math.ceil(len(thumbs) / cols)
sheet = Image.new("RGB", (cols*660, rows*390), BG)
for i, img in enumerate(thumbs):
    sheet.paste(img, ((i % cols)*660, (i // cols)*390))
sheet.save(ROOT / "contact_sheet.png")

print(f"Generated {len(generated)} PNG visuals.")
print(f"Korean font selected: {FONT}")
print(f"PDF: {pdf_path}")
print(f"Contact sheet: {ROOT / 'contact_sheet.png'}")
