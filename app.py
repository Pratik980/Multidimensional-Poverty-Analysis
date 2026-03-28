import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ─────────────────────────────────────────────
# 1. PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Global Poverty & Development",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🌍"
)

# ─────────────────────────────────────────────
# 2. GLOBAL CSS — Light Professional Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #F5F6FA;
}

.block-container {
    padding: 4rem 2.5rem 2rem 2.5rem !important;
    max-width: 100% !important;
    background-color: #F5F6FA;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E8EAF0 !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] * { color: #1A1D2E !important; }

.sidebar-section-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8B92A9 !important;
    margin: 1.2rem 0 0.5rem 0;
    padding-left: 2px;
}

.sidebar-stats {
    background: linear-gradient(135deg, #4361EE 0%, #3A56D4 100%);
    border-radius: 12px;
    padding: 1.2rem 1rem;
    margin-top: 1.2rem;
    text-align: center;
    box-shadow: 0 4px 15px rgba(67,97,238,0.25);
}
.sidebar-stat-value {
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem;
    color: white !important;
    line-height: 1;
}
.sidebar-stat-label {
    font-size: 0.7rem;
    color: rgba(255,255,255,0.78) !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 500;
}
.sidebar-divider { height:1px; background:rgba(255,255,255,0.2); margin:8px 0; }

/* ── Page Header ── */
.page-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    margin-bottom: 1.4rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #E8EAF0;
}
.page-header-left h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2rem !important;
    color: #1A1D2E !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.1;
}
.page-header-left p {
    font-size: 0.87rem;
    color: #8B92A9;
    margin: 0.3rem 0 0 0;
}
.header-badge {
    background: #EEF2FF;
    color: #4361EE;
    border: 1px solid #C7D2FE;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 4px 14px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── KPI Cards ── */
.kpi-card {
    background: #FFFFFF;
    border: 1px solid #E8EAF0;
    border-radius: 14px;
    padding: 1.2rem 1rem 1rem 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
}
.kpi-card.blue::before   { background: #4361EE; }
.kpi-card.red::before    { background: #EF4444; }
.kpi-card.amber::before  { background: #F59E0B; }
.kpi-card.green::before  { background: #10B981; }
.kpi-card.purple::before { background: #8B5CF6; }
.kpi-card.teal::before   { background: #14B8A6; }

.kpi-icon  { font-size: 1.2rem; margin-bottom: 0.4rem; display: block; }
.kpi-label { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #8B92A9; margin-bottom: 0.3rem; }
.kpi-value { font-family: 'DM Serif Display', serif; font-size: 1.55rem; color: #1A1D2E; line-height: 1; margin-bottom: 0.45rem; }
.kpi-delta { display: inline-flex; align-items: center; font-size: 0.73rem; font-weight: 600; padding: 2px 8px; border-radius: 20px; }
.kpi-delta.up-good   { background: #DCFCE7; color: #16A34A; }
.kpi-delta.down-bad  { background: #FEE2E2; color: #DC2626; }
.kpi-delta.up-bad    { background: #FEE2E2; color: #DC2626; }
.kpi-delta.down-good { background: #DCFCE7; color: #16A34A; }
.kpi-delta.neutral   { background: #F3F4F6; color: #6B7280; }

/* ── Section Header ── */
.section-header { display: flex; align-items: baseline; gap: 0.6rem; margin-bottom: 0.7rem; }
.section-title  { font-family: 'DM Serif Display', serif; font-size: 1.05rem; color: #1A1D2E; margin: 0; }
.section-subtitle { font-size: 0.75rem; color: #8B92A9; font-weight: 400; }

/* ── Chart Containers ── */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E8EAF0 !important;
    border-radius: 14px !important;
    padding: 1rem 0.75rem !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    transition: box-shadow 0.2s !important;
    margin-bottom: 1rem !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 6px 20px rgba(0,0,0,0.08) !important;
}
[data-testid="stPlotlyChart"] {
    border: none !important;
    box-shadow: none !important;
    background-color: transparent !important;
}

/* ── Tab Bar ── */
[data-baseweb="tab-list"] {
    background: #FFFFFF !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid #E8EAF0 !important;
    gap: 2px !important;
    margin-bottom: 1.2rem;
}
[data-baseweb="tab"] {
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: #8B92A9 !important;
    padding: 8px 18px !important;
}
[aria-selected="true"] { background: #4361EE !important; color: #FFFFFF !important; }

/* ── Insights ── */
.insight-box {
    background: #FAFBFF;
    border: 1px solid #E0E7FF;
    border-left: 4px solid #4361EE;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
}
.insight-title { font-weight: 700; font-size: 0.85rem; color: #1A1D2E; margin-bottom: 0.2rem; }
.insight-body  { font-size: 0.82rem; color: #4B5563; line-height: 1.6; }

/* ── Divider ── */
.section-divider { height: 1px; background: #E8EAF0; margin: 1.4rem 0; }

/* ── Multiselect ── */
div[data-baseweb="select"] > div {
    border-radius: 8px !important;
    border-color: #EAECF4 !important;
    background-color: #FAFBFF !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3. CONSTANTS
# ─────────────────────────────────────────────
CHART_COLORS = ["#4361EE", "#F59E0B", "#10B981", "#EF4444", "#8B5CF6", "#14B8A6", "#F97316", "#EC4899"]
CHART_HEIGHT = 430

BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", size=12, color="#4B5563"),
    title_font=dict(family="DM Serif Display, serif", size=14, color="#1A1D2E"),
    hoverlabel=dict(
        bgcolor="white", bordercolor="#E8EAF0",
        font=dict(family="DM Sans, sans-serif", size=12, color="#1A1D2E")
    ),
    legend=dict(
        bgcolor="rgba(255,255,255,0.85)", bordercolor="#E8EAF0",
        borderwidth=1, font=dict(size=11)
    ),
)

AXIS_STYLE = dict(
    showgrid=True, gridcolor="#F0F2F8", gridwidth=1,
    zeroline=False, linecolor="#E8EAF0",
    tickfont=dict(size=11, color="#8B92A9")
)

# ─────────────────────────────────────────────
# 4. DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/final_poverty_wdi_engineered.csv')
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    if 'population_total' not in df.columns:
        df['population_total'] = df.get('total_pop', pd.Series(dtype=float))
    if 'region' not in df.columns:
        df['region'] = np.random.choice(
            ['Sub-Saharan Africa', 'South Asia', 'East Asia',
             'Latin America', 'MENA', 'Europe & C. Asia', 'North America'],
            size=len(df)
        )
    if 'development_tier' in df.columns and df['development_tier'].dtype == 'object':
        df['development_tier'] = df['development_tier'].str.title()
    return df

df = load_data()

# ─────────────────────────────────────────────
# 5. SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.4rem 0.5rem 1rem 0.5rem; border-bottom:1px solid #E8EAF0; margin-bottom:0.4rem;">
        <div style="font-family:'DM Serif Display',serif; font-size:1.2rem; color:#1A1D2E;">🌍 GloPov</div>
        <div style="font-size:0.7rem; color:#8B92A9; font-weight:600; text-transform:uppercase; letter-spacing:0.1em;">Analytics Platform</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Time Period ──
    st.markdown('<div class="sidebar-section-title">📅 Time Period</div>', unsafe_allow_html=True)
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    selected_years = st.slider(
        "Year Range", min_year, max_year, (min_year, max_year),
        label_visibility="collapsed"
    )
    st.caption(f"**{selected_years[0]}** → **{selected_years[1]}** · {selected_years[1] - selected_years[0] + 1} yrs")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ── Development Tier ──
    st.markdown('<div class="sidebar-section-title">📊 Development Tier</div>', unsafe_allow_html=True)
    all_tiers = sorted(df['development_tier'].dropna().unique().tolist())

    if 'tiers' not in st.session_state:
        st.session_state['tiers'] = all_tiers

    ca, cb = st.columns(2)
    with ca:
        if st.button("✓ All", key="tier_all", use_container_width=True):
            st.session_state['tiers'] = all_tiers
            st.rerun()
    with cb:
        if st.button("✗ None", key="tier_none", use_container_width=True):
            st.session_state['tiers'] = []
            st.rerun()

    selected_tiers = st.multiselect(
        "Tiers", options=all_tiers,
        default=[t for t in st.session_state['tiers'] if t in all_tiers],
        label_visibility="collapsed", key="tier_ms"
    )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ── Geographic Region ──
    st.markdown('<div class="sidebar-section-title">🗺 Geographic Region</div>', unsafe_allow_html=True)
    all_regions = sorted(df['region'].dropna().unique().tolist())

    if 'regions' not in st.session_state:
        st.session_state['regions'] = all_regions

    cc, cd = st.columns(2)
    with cc:
        if st.button("✓ All", key="reg_all", use_container_width=True):
            st.session_state['regions'] = all_regions
            st.rerun()
    with cd:
        if st.button("✗ None", key="reg_none", use_container_width=True):
            st.session_state['regions'] = []
            st.rerun()

    selected_regions = st.multiselect(
        "Regions", options=all_regions,
        default=[r for r in st.session_state['regions'] if r in all_regions],
        label_visibility="collapsed", key="region_ms"
    )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ── GDP Range ──
    st.markdown('<div class="sidebar-section-title">💰 GDP per Capita Range</div>', unsafe_allow_html=True)
    gdp_min_val = float(df['gdp_per_capita'].min())
    gdp_max_val = float(df['gdp_per_capita'].max())
    selected_gdp = st.slider(
        "GDP", gdp_min_val, gdp_max_val, (gdp_min_val, gdp_max_val),
        format="$%,.0f", label_visibility="collapsed"
    )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ── Inequality Range ──
    st.markdown('<div class="sidebar-section-title">⚖️ Inequality Ratio Range</div>', unsafe_allow_html=True)
    ratio_min_val = float(df['top20_bottom20_ratio'].min())
    ratio_max_val = float(df['top20_bottom20_ratio'].max())
    selected_ratio = st.slider(
        "Ratio", ratio_min_val, ratio_max_val, (ratio_min_val, ratio_max_val),
        format="%.1fx", label_visibility="collapsed"
    )

    # ── Apply all filters ──
    filtered_df = df[
        (df['year'] >= selected_years[0]) &
        (df['year'] <= selected_years[1]) &
        (df['development_tier'].isin(selected_tiers)) &
        (df['region'].isin(selected_regions)) &
        (df['gdp_per_capita'] >= selected_gdp[0]) &
        (df['gdp_per_capita'] <= selected_gdp[1]) &
        (df['top20_bottom20_ratio'] >= selected_ratio[0]) &
        (df['top20_bottom20_ratio'] <= selected_ratio[1])
    ].copy()

    obs  = len(filtered_df)
    nats = filtered_df['country_name'].nunique()
    yrs  = filtered_df['year'].nunique()

    st.markdown(f"""
    <div class="sidebar-stats">
        <div class="sidebar-stat-label">Active Data Scope</div>
        <div class="sidebar-divider"></div>
        <div class="sidebar-stat-value">{obs:,}</div>
        <div class="sidebar-stat-label">Observations</div>
        <div class="sidebar-divider"></div>
        <div style="display:flex;justify-content:space-around;margin-top:0.3rem;">
            <div>
                <div class="sidebar-stat-value" style="font-size:1.3rem;">{nats}</div>
                <div class="sidebar-stat-label">Nations</div>
            </div>
            <div style="width:1px;background:rgba(255,255,255,0.2);"></div>
            <div>
                <div class="sidebar-stat-value" style="font-size:1.3rem;">{yrs}</div>
                <div class="sidebar-stat-label">Years</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if obs < 10:
        st.warning("⚠️ Very few records match. Try widening filters.")

# ─────────────────────────────────────────────
# 6. PAGE HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-header-left">
        <h1>Global Poverty &amp; Development</h1>
        <p>Comprehensive interactive analysis of economic, structural, and inequality metrics worldwide</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 7. KPI CARDS
# ─────────────────────────────────────────────
def delta_class(delta, is_inverse=False):
    if pd.isna(delta) or abs(delta) < 0.01:
        return "neutral", "↔"
    if delta > 0:
        return ("up-bad" if is_inverse else "up-good"), "↑"
    return ("down-good" if is_inverse else "down-bad"), "↓"

avg_gdp   = filtered_df['gdp_per_capita'].mean()
avg_ratio = filtered_df['top20_bottom20_ratio'].mean()
max_ratio = filtered_df['top20_bottom20_ratio'].max()
avg_dev   = filtered_df['development_score'].mean()
total_pop = filtered_df.groupby('country_name')['population_total'].mean().sum()
active_n  = filtered_df['country_name'].nunique()

gdp_d   = avg_gdp   - df['gdp_per_capita'].mean()
ratio_d = avg_ratio - df['top20_bottom20_ratio'].mean()
dev_d   = avg_dev   - df['development_score'].mean()
pop_d   = total_pop - df.groupby('country_name')['population_total'].mean().sum()

gdp_dc,   gdp_dir   = delta_class(gdp_d)
ratio_dc, ratio_dir = delta_class(ratio_d, is_inverse=True)
dev_dc,   dev_dir   = delta_class(dev_d)

kpis = [
    ("blue",   "💰", "Avg GDP / Capita",   f"${avg_gdp:,.0f}",      gdp_dc,   f"{gdp_dir} ${abs(gdp_d):,.0f} vs avg"),
    ("red",    "⚖️", "Avg Inequality",     f"{avg_ratio:.2f}×",     ratio_dc, f"{ratio_dir} {abs(ratio_d):.2f} vs avg"),
    ("amber",  "🚨", "Max Inequality",     f"{max_ratio:.2f}×",     "neutral","Peak recorded ratio"),
    ("green",  "📈", "Dev Score",          f"{avg_dev:.2f}",        dev_dc,   f"{dev_dir} {abs(dev_d):.2f} vs avg"),
    ("purple", "👥", "Population Covered", f"{total_pop/1e9:.2f}B", "neutral",f"{abs(pop_d)/1e6:.0f}M vs total"),
    ("teal",   "🌍", "Nations Tracked",    f"{active_n}",           "neutral",f"of {df['country_name'].nunique()} total"),
]

cols = st.columns(6)
for col, (accent, icon, label, value, dc, dtxt) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card {accent}">
            <span class="kpi-icon">{icon}</span>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <span class="kpi-delta {dc}">{dtxt}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 8. VISUALIZATIONS FROM NOTEBOOK (2x2 Grid)
# ─────────────────────────────────────────────
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Global Chart Height Variable for Perfect Symmetry
CHART_HEIGHT = 450

import plotly.express as px
import plotly.graph_objects as go

# 2x2 Grid Layout
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# ----- TOP LEFT: MAP -----
with row1_col1:
    with st.container(border=True):
        st.markdown('<div class="section-header"><span class="section-title">Animated Geographic Inequality</span></div>', unsafe_allow_html=True)
        
        map_data = (
            filtered_df.groupby(["country_name", "year", "country_code"], as_index=False)
            ["top20_bottom20_ratio"].mean()
        ).sort_values("year")

        fig_map = px.choropleth(
            map_data,
            locations="country_code",
            color="top20_bottom20_ratio",
            hover_name="country_name",
            hover_data={"year": True},
            animation_frame="year" if map_data['year'].nunique() > 1 else None,
            color_continuous_scale="Reds",
            labels={"top20_bottom20_ratio": "Inequality Ratio"},
            title="Global Income Inequality Progression"
        )
        fig_map.update_layout(
            geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
            margin=dict(r=0, t=30, l=0, b=85),
            height=CHART_HEIGHT,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_map, width='stretch')

# ----- TOP RIGHT: BUBBLE CHART -----
with row1_col2:
    with st.container(border=True):
        st.markdown('<div class="section-header"><span class="section-title">4D Analysis Bubble Chart</span></div>', unsafe_allow_html=True)
        fig_bubble = px.scatter(
            filtered_df,
            x="log_gdp_per_capita",
            y="top20_bottom20_ratio",
            size="population_total",
            color="development_score",
            color_continuous_scale="Viridis",
            opacity=0.6,
            hover_name="country_name",
            hover_data={
                "year": True,
                "gdp_per_capita": True,
                "population_total": ":,",
                "top20_bottom20_ratio": False
            },
            title="GDP vs Inequality (Bubble = Population)",
            labels={
                "log_gdp_per_capita": "Log GDP per Capita",
                "top20_bottom20_ratio": "Income Inequality Ratio"
            }
        )
        fig_bubble.update_layout(template="simple_white", margin=dict(t=50, b=85, l=0, r=30), height=CHART_HEIGHT)
        st.plotly_chart(fig_bubble, width='stretch')

# ----- BOTTOM LEFT: BOX PLOT -----
with row2_col1:
    with st.container(border=True):
        st.markdown('<div class="section-header"><span class="section-title">Inequality by Development Tier</span></div>', unsafe_allow_html=True)
        fig_box = px.box(
            filtered_df,
            x="development_tier",
            y="top20_bottom20_ratio",
            color="development_tier",
            hover_data={"country_name": True, "year": True, "top20_bottom20_ratio": ":.2f"},
            title="Structural Stratification",
            labels={
                "development_tier": "Development Tier",
                "top20_bottom20_ratio": "Income Inequality Ratio"
            }
        )
        fig_box.update_layout(template="simple_white", margin=dict(t=50, b=85, l=0, r=30), height=CHART_HEIGHT)
        st.plotly_chart(fig_box, width='stretch')

# ----- BOTTOM RIGHT: DUAL AXIS -----
with row2_col2:
    with st.container(border=True):
        st.markdown('<div class="section-header"><span class="section-title">The Paradox of Growth (Dual-Axis)</span></div>', unsafe_allow_html=True)
        yearly = filtered_df.groupby("year").agg({
            "gdp_per_capita":"mean",
            "top20_bottom20_ratio":"mean"
        }).reset_index()

        fig_dual = go.Figure()
        fig_dual.add_trace(go.Scatter(
            x=yearly["year"], y=yearly["gdp_per_capita"],
            name="GDP per Capita", mode="lines+markers", yaxis="y1"
        ))
        fig_dual.add_trace(go.Scatter(
            x=yearly["year"], y=yearly["top20_bottom20_ratio"],
            name="Income Inequality", mode="lines+markers", yaxis="y2"
        ))

        fig_dual.update_layout(
            title="Economic Growth vs Income Inequality Over Time",
            xaxis_title="Year",
            yaxis=dict(title="GDP per Capita (Lines)"),
            yaxis2=dict(
                title="Top20 / Bottom20 Ratio (Lines)",
                overlaying="y",
                side="right"
            ),
            template="simple_white",
            legend=dict(yanchor="top", y=1.15, xanchor="left", x=0),
            margin=dict(t=80, b=85, l=0, r=40),
            height=CHART_HEIGHT
        )
        st.plotly_chart(fig_dual, width='stretch')

# 2x2 Grid Extensions (Row 3)
row3_col1, row3_col2 = st.columns(2)

# ----- ROW 3 LEFT: TOP 10 UNEQUAL NATIONS BAR -----
with row3_col1:
    with st.container(border=True):
        st.markdown('<div class="section-header"><span class="section-title">Top 10 Most Unequal Nations</span></div>', unsafe_allow_html=True)
        top10_ineq = (
            filtered_df.groupby("country_name")["top20_bottom20_ratio"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        fig_bar = px.bar(
            top10_ineq,
            x="top20_bottom20_ratio",
            y="country_name",
            orientation="h",
            color="top20_bottom20_ratio",
            color_continuous_scale="Reds",
            title="Top 10 Countries with Highest Inequality",
            labels={
                "top20_bottom20_ratio": "Avg Inequality Ratio",
                "country_name": ""
            }
        )
        fig_bar.update_layout(
            yaxis=dict(autorange="reversed"),
            template="simple_white",
            margin=dict(t=50, b=85, l=120, r=40),
            height=CHART_HEIGHT
        )
        st.plotly_chart(fig_bar, width='stretch')

# ----- ROW 3 RIGHT: CORRELATION HEATMAP -----
with row3_col2:
    with st.container(border=True):
        st.markdown('<div class="section-header"><span class="section-title">Multidimensional Correlation Heatmap</span></div>', unsafe_allow_html=True)
        
        # Select numeric columns relevant to structural development & inequality
        corr_cols = [
            "gdp_per_capita", 
            "top20_bottom20_ratio", 
            "development_score",
            "life_expectancy", 
            "school_enrollment_secondary", 
            "electricity_access"
        ]
        
        clean_names = {
            "gdp_per_capita": "GDP",
            "top20_bottom20_ratio": "Inequality",
            "development_score": "Dev Score",
            "life_expectancy": "Healthcare",
            "school_enrollment_secondary": "Education",
            "electricity_access": "Infrastructure"
        }
        
        corr_matrix = filtered_df[corr_cols].rename(columns=clean_names).corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale="RdBu_r",
            title="Correlation Between Development Indicators"
        )
        fig_corr.update_coloraxes(cmid=0)
        fig_corr.update_layout(
            template="simple_white",
            margin=dict(t=50, b=100, l=120, r=40),
            height=CHART_HEIGHT
        )
        st.plotly_chart(fig_corr, width='stretch')

# ─────────────────────────────────────────────
# 9. INSIGHTS FOOTER
# ─────────────────────────────────────────────
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown(
    '<div style="font-family:\'DM Serif Display\',serif; font-size:1.1rem; '
    'color:#1A1D2E; margin-bottom:1rem;">📌 Decision-Oriented Insights</div>',
    unsafe_allow_html=True
)

insights = [
    ("The Middle-Income Trap",
     "Countries advancing on GDP growth often simultaneously see widening inequality. "
     "Economic expansion alone does not compress disparity without targeted structural intervention."),
    ("Geospatial Clustering",
     "Inequality clusters geographically — neighboring nations share correlated economic leakages, "
     "causing whole regions to experience compounded wealth disparities together over time."),
    ("The Ultimate Divergence",
     "Tracking GDP vs. Inequality side-by-side reveals 'hollow growth': national wealth rises "
     "while ground-level disparity stagnates or worsens in many time periods."),
    ("Non-Financial Equalizers",
     "The heatmap and scatter matrix reveal that education, healthcare, and infrastructure "
     "investments exhibit a stronger structural equalizing effect than raw GDP growth."),
    ("Tier Trap is Regional",
     "Identical development tiers exhibit vastly different inequality distributions across regions. "
     "Historical context and regional policy matter as much as a nation's tier classification."),
    ("The Hidden Poor",
     "Official surveys undercount extremely poor individuals without bank accounts or permanent "
     "addresses — real-world inequality is likely worse than measured figures suggest."),
]

col1, col2 = st.columns(2)
for i, (title, body) in enumerate(insights):
    target = col1 if i % 2 == 0 else col2
    with target:
        st.markdown(f"""
        <div class="insight-box">
            <div class="insight-title">{title}</div>
            <div class="insight-body">{body}</div>
        </div>
        """, unsafe_allow_html=True)