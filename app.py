"""中學英文部資訊科技科組年度匯報 Dashboard。"""

from __future__ import annotations

from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="中學資訊科技科組年度匯報",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=Noto+Sans+TC:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #10243e;
        --muted: #5f7289;
        --paper: #f3f7f8;
        --panel: rgba(255, 255, 255, 0.88);
        --line: rgba(15, 56, 89, 0.12);
        --cyan: #00a9c7;
        --teal: #008f7a;
        --lime: #9ccc3c;
        --coral: #ff6b4a;
        --navy: #071c33;
    }

    html, body, [class*="css"], .stApp {
        font-family: "IBM Plex Sans", "Noto Sans TC", sans-serif;
    }

    .stApp {
        color: var(--ink);
        background:
            radial-gradient(circle at 92% 5%, rgba(0, 169, 199, 0.09), transparent 24rem),
            radial-gradient(circle at 12% 72%, rgba(156, 204, 60, 0.08), transparent 28rem),
            var(--paper);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1440px;
        padding-top: 1.35rem;
        padding-bottom: 4rem;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(132, 224, 238, 0.14);
        background:
            linear-gradient(160deg, rgba(9, 37, 62, 0.98), rgba(4, 19, 35, 0.99)),
            #071c33;
    }

    [data-testid="stSidebar"] * {
        color: #dceaf2;
    }

    [data-testid="stSidebar"] h2 {
        color: white;
        font-size: 1.15rem;
        letter-spacing: -0.02em;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label {
        margin: 0.28rem 0;
        padding: 0.55rem 0.65rem;
        border: 1px solid transparent;
        border-radius: 0.75rem;
        transition: 150ms ease;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        border-color: rgba(103, 232, 249, 0.25);
        background: rgba(103, 232, 249, 0.07);
    }

    .section-heading {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 1rem;
        margin: 2rem 0 1.15rem;
        padding-bottom: 0.9rem;
        border-bottom: 1px solid var(--line);
    }

    .section-kicker {
        margin: 0 0 0.28rem;
        color: var(--cyan);
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .section-heading h1 {
        margin: 0;
        color: var(--ink);
        font-size: clamp(2rem, 4vw, 3.25rem);
        line-height: 1;
        letter-spacing: -0.055em;
    }

    .section-heading p:last-child {
        max-width: 520px;
        margin: 0 0 0.18rem;
        color: var(--muted);
        font-size: 0.93rem;
        text-align: right;
    }

    h2, h3, h4 {
        color: var(--ink) !important;
        letter-spacing: -0.025em;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid rgba(15, 56, 89, 0.1) !important;
        border-radius: 1.1rem !important;
        background: var(--panel);
        box-shadow: 0 12px 35px rgba(9, 40, 66, 0.065);
        transition: transform 160ms ease, box-shadow 160ms ease;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 42px rgba(9, 40, 66, 0.1);
    }

    [data-testid="stMetric"] {
        min-height: 112px;
        padding: 1rem 1.05rem;
        border: 1px solid var(--line);
        border-top: 4px solid var(--cyan);
        border-radius: 1rem;
        background: rgba(255, 255, 255, 0.9);
        box-shadow: 0 10px 26px rgba(9, 40, 66, 0.055);
    }

    [data-testid="stMetricValue"] {
        color: var(--navy);
        font-weight: 700;
        letter-spacing: -0.04em;
    }

    [data-testid="stDataFrame"],
    [data-testid="stPlotlyChart"] {
        overflow: hidden;
        border: 1px solid var(--line);
        border-radius: 1rem;
        background: white;
        box-shadow: 0 10px 30px rgba(9, 40, 66, 0.055);
    }

    [data-testid="stExpander"] {
        border: 1px solid var(--line);
        border-radius: 0.9rem;
        background: rgba(255, 255, 255, 0.78);
    }

    [data-testid="stAlert"] {
        border: 0;
        border-left: 4px solid var(--cyan);
        border-radius: 0.75rem;
    }

    .stMultiSelect [data-baseweb="select"] > div {
        border-color: rgba(15, 56, 89, 0.16);
        border-radius: 0.8rem;
        background: white;
    }

    @media (max-width: 760px) {
        [data-testid="stMainBlockContainer"] { padding-top: 0.75rem; }
        .section-heading { display: block; }
        .section-heading p:last-child { margin-top: 0.65rem; text-align: left; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


CURRICULUM = [
    ("F1", "數碼基礎、Office、AI 短片、LEGO EV3", "建立數碼表達與工程解難基礎"),
    ("F2", "Micro:bit、AutoCAD、Fusion 360", "連結編程、感測器與 3D 設計"),
    ("F3", "計算機概論、C++、ESP32", "以智能裝置串連語法、硬件與安全"),
    ("F4", "Adobe 多媒體、ESP32 進階", "發展智慧校園原型與多媒體表達"),
    ("F5", "Excel／MOS、Python、HTML／CSS", "建立數據處理及網頁發布能力"),
    ("F6", "MySQL、Excel／Python 數據分析", "完成畢業數據專題與分析報告"),
]

ACHIEVEMENTS = pd.DataFrame(
    [
        ["澳門信息學奧林匹克選拔賽", "本地", "5 銀、1 銅", "演算法／程式設計"],
        ["微信小程序全球創新挑戰賽（澳門區）", "區域", "特等獎、一等獎", "小程序／創新實作"],
        ["全澳學生手機網站技術技能比賽", "本地", "亞軍", "網站開發"],
        ["大灣區青少年人工智能及網絡安全挑戰賽", "區域", "智慧實踐獎、卓越商業應用獎", "AI／網絡安全"],
        ["ICOA 2026", "國際", "入選澳門代表隊", "人工智能／網絡"],
    ],
    columns=["賽事", "層級", "成果", "能力範疇"],
)

HERO_TEMPLATE = Path(__file__).with_name("assets").joinpath("p5_hero.html")
P5_CDN_URL = "https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"


@st.cache_data(show_spinner=False)
def load_p5_source() -> str:
    """Fetch p5.js server-side so the component does not depend on iframe CDN access."""
    request = Request(P5_CDN_URL, headers={"User-Agent": "CDSJ5-IT-Dashboard/1.0"})
    with urlopen(request, timeout=10) as response:
        source = response.read().decode("utf-8")
    if "p5" not in source or len(source) < 100_000:
        raise RuntimeError("Invalid p5.js response")
    return source.replace("</script", "<\\/script")


def render_p5_hero(section: str) -> None:
    """Render the p5.js curriculum flow visual at the top of the dashboard."""
    hero_html = HERO_TEMPLATE.read_text(encoding="utf-8")
    try:
        p5_source = load_p5_source()
        p5_script = f"<script>{p5_source}</script>"
    except Exception as exc:
        p5_script = (
            '<div class="p5-error">p5.js 載入失敗：請檢查網絡後重新整理。</div>'
            f"<!-- {type(exc).__name__} -->"
        )
    hero_html = hero_html.replace("__P5_SCRIPT__", p5_script).replace(
        "__SECTION__", section
    )
    components.html(hero_html, height=306, scrolling=False)


def page_header(title: str, subtitle: str) -> None:
    """Render a consistent page heading."""
    st.markdown(
        f"""
        <div class="section-heading">
            <div>
                <p class="section-kicker">Annual Report · 2025–2026</p>
                <h1>{title}</h1>
            </div>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_curriculum() -> None:
    page_header("課程發展", "F1–F6 縱向課程路線與年度重點")

    st.markdown(
        """
        將零散工具教學整理為一條**對接基力、重視實作、逐級銜接**的課程路線。
        """
    )

    st.subheader("本年度三項重點工作")
    focus1, focus2, focus3 = st.columns(3)
    with focus1:
        with st.container(border=True):
            st.markdown("#### ① 課程及基力對標")
            st.write("完成課程梳理及基本學力要求對標。")
    with focus2:
        with st.container(border=True):
            st.markdown("#### ② 專題實作與多元評核")
            st.write("以程式、硬件及作品呈現學習成果。")
    with focus3:
        with st.container(border=True):
            st.markdown("#### ③ 課程與拔尖連結")
            st.write("由課堂延伸至比賽及代表隊培育。")

    st.subheader("F1–F6 課程路線")

    for grade, content, outcome in CURRICULUM:
        with st.container(border=True):
            left, right = st.columns([1, 5])
            left.subheader(grade)
            right.markdown(f"**核心內容：** {content}")
            right.markdown(f"**預期成果：** {outcome}")

    st.info(
        "發展主線：數碼基礎 → 編程與硬件 → 多媒體與網頁 → 數據分析與專題。"
    )

    with st.expander("查看基本學力要求對標重點"):
        st.markdown(
            """
            - **概念與認知：** 電腦架構、演算法、物聯網、人工智能及數據概念；
            - **應用與創作：** 程式設計、硬件控制、3D 建模、多媒體、網頁及數據分析；
            - **溝通與合作：** 專題匯報、共同解難、數碼作品展示及跨學科學習；
            - **道德與責任：** 資訊安全、密碼與私隱、知識產權、AI 倫理及負責任使用科技。

            課程中特別補強生成式 AI、物聯網與感測器、程式設計與演算法、
            數據處理與視覺化，以及資訊安全與 AI 倫理。
            """
        )

    with st.expander("查看專題式學習與評核安排"):
        st.markdown(
            """
            各級逐步安排 EV3 機械人解難、Micro:bit／ESP32 感測器作品、
            C++ 程式設計、Office 與多媒體作品、網頁、小程序及數據分析專題。

            評核方向由單一測驗擴展至「平時表現＋實作／專題」，觀察學生是否能夠：

            1. 理解及分析問題；
            2. 設計可行方案；
            3. 編寫、測試與除錯；
            4. 展示作品並解釋設計決定；
            5. 遵守私隱、版權和安全要求。
            """
        )


def render_achievements() -> None:
    page_header("競賽拔尖", "由普及課程延伸至專題實作、比賽及代表隊培育")

    col1, col2, col3 = st.columns(3)
    col1.metric("示範賽事項目", len(ACHIEVEMENTS))
    col2.metric("涵蓋層級", ACHIEVEMENTS["層級"].nunique())
    col3.metric("能力範疇", ACHIEVEMENTS["能力範疇"].nunique())

    level_filter = st.multiselect(
        "按賽事層級篩選",
        options=ACHIEVEMENTS["層級"].unique(),
        default=list(ACHIEVEMENTS["層級"].unique()),
    )
    filtered = ACHIEVEMENTS[ACHIEVEMENTS["層級"].isin(level_filter)]
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    st.caption("資料整理自現有科組競賽紀錄；如日後資料更新，再同步調整。")

    st.subheader("成果所反映的教學成效")
    st.markdown(
        """
        **普及課程 → 專題實作 → 競賽拔尖 → 代表隊培育**
        """
    )

    with st.expander("本科組最滿意之處"):
        st.markdown(
            """
            課程、基力、實作及拔尖成果已形成清晰路線，並能回答：
            **學甚麼、做甚麼、如何繼續發展。**
            """
        )


def render_transition() -> None:
    page_header("小中銜接", "P6–F1 銜接能力、診斷任務及分層支援")

    st.subheader("目前情況")
    st.markdown(
        """
        **改善重點：建立「P6–F1 銜接能力清單＋開學診斷任務」。**
        減少重複內容，並及早識別需要支援或拔尖的學生。
        """
    )

    st.subheader("開學診斷任務清單")
    checklist = [
        "檔案及資料夾管理",
        "英文輸入與文件排版",
        "簡報及多媒體表達",
        "順序、條件與循環概念",
        "基本程式除錯",
        "感測器及輸入／輸出概念",
        "密碼、私隱及知識產權",
    ]
    cols = st.columns(2)
    for index, item in enumerate(checklist):
        cols[index % 2].checkbox(item, key=f"transition_{index}")

    st.subheader("學生分組邏輯")
    foundation, advanced, elite = st.columns(3)
    with foundation:
        st.markdown("### 基礎組")
        st.write("補足檔案管理、Office 及基礎程式概念。")
    with advanced:
        st.markdown("### 進階組")
        st.write("直接進入 EV3、感測器及專題任務。")
    with elite:
        st.markdown("### 拔尖組")
        st.write("加入 AI、進階編程或競賽延伸任務。")

def render_analytics() -> None:
    page_header("數據評鑑", "日常監測課程成效、學生達標及科組行動")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("實作評核合格率", "70%+", help="周年計劃所載示範指標")
    kpi2.metric("基礎概念掌握率", "85%", help="周年計劃所載示範指標")
    kpi3.metric("改進方案完成率", "95%", help="周年計劃所載示範指標")
    kpi4.metric("F1–F6 覆蓋", "6 級", help="中學英文部課程級別")

    st.caption(
        "以上百分比來自科組周年計劃的執行情況記錄；日後如有更新資料，"
        "再連結原始成績、作品量規及班級數據。"
    )

    st.subheader("達標率概覽")

    demo = pd.DataFrame(
        {
            "年級": ["F1", "F2", "F3", "F4", "F5", "F6"],
            "實作合格率": [72, 76, 81, 79, 86, 83],
            "概念掌握率": [78, 82, 85, 84, 88, 87],
        }
    )
    chart_data = demo.melt(
        id_vars="年級", var_name="指標", value_name="百分比"
    )
    bar_chart = px.bar(
        chart_data,
        x="年級",
        y="百分比",
        color="指標",
        barmode="group",
        range_y=[0, 100],
        title="各級達標率（示範數據）",
        color_discrete_sequence=["#2F6BFF", "#22A06B"],
    )
    st.plotly_chart(bar_chart, use_container_width=True)

    score_demo = pd.DataFrame(
        {
            "分數": [
                52, 58, 61, 64, 66, 68, 70, 72, 74, 75, 76, 78, 79, 80,
                82, 83, 84, 85, 86, 88, 90, 91, 93, 95,
            ]
        }
    )
    histogram = px.histogram(
        score_demo,
        x="分數",
        nbins=10,
        title="學生成績分布（示範數據）",
        color_discrete_sequence=["#7C3AED"],
    )
    st.plotly_chart(histogram, use_container_width=True)
    st.warning("所有圖表數值目前均為介面示範，不應用作正式匯報。")

    st.subheader("下一步")
    st.error("核心改善：建立更一致、更可量化的課程評鑑和教學證據系統。")
    problem_col, action_col = st.columns(2)
    with problem_col:
        st.markdown("#### 目前需要處理")
        st.markdown(
            """
            - 同級不同教師的進度與評分仍可能不一致；
            - 學生作品未完全採用共同量規；
            - 觀課、議課及課程改進紀錄仍不夠完整；
            - 部分百分比未直接連結原始成績或作品數據；
            - 競賽成果突出，但一般學生的整體增值未充分呈現。
            """
        )
    with action_col:
        st.markdown("#### 來年具體做法")
        st.markdown(
            """
            1. 每級訂立一項核心代表作品；
            2. 同級共用核心進度、題型及評量量規；
            3. 每月抽取各班 3–5 份作品共同校準；
            4. 每學期記錄達標率、優良率、常見錯誤及前後測差異；
            5. 建立教案、量規、作品及觀課紀錄的共用資源庫；
            6. 課程劃分共同必修、選修拓展及競賽拔尖三層。
            """
        )

    with st.expander("科組所需支援"):
        st.markdown(
            """
            - 每月一次約 30 分鐘的固定科組校準時間；
            - 統一的雲端資源庫與作品記錄表；
            - 學校層面支持跨級共同備課及學生作品交接。
            """
        )


PAGES = {
    "課程發展": render_curriculum,
    "競賽拔尖": render_achievements,
    "小中銜接": render_transition,
    "數據評鑑": render_analytics,
}

with st.sidebar:
    st.header("中學資訊科技科組")
    st.caption("年度匯報與日常觀測 Dashboard")
    selected_page = st.radio("導覽", options=list(PAGES), index=0)
    st.divider()
    st.caption("Annual Report Dashboard v0.6 · Fullscreen Lines")

render_p5_hero(selected_page)
PAGES[selected_page]()
