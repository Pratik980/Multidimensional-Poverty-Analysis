import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="Global Inequality Dashboard", layout="wide")

st.title("🌍 Global Development & Inequality Dashboard")

# -----------------------
# LOAD DATA (ROBUST PATH)
# -----------------------
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "final_poverty_wdi_engineered.csv")
    df = pd.read_csv(file_path)

    # -----------------------
    # SAFETY CHECKS (avoid crashes)
    # -----------------------
    df.columns = df.columns.str.lower().str.strip()

    # Rename if needed (in case your dataset varies slightly)
    rename_map = {
        "country": "country_name",
        "countrycode": "country_code",
        "year": "year"
    }
    df = df.rename(columns=rename_map)

    return df

df = load_data()

# -----------------------
# SIDEBAR FILTERS
# -----------------------
st.sidebar.header("🔍 Filters")

year_min = int(df["year"].min())
year_max = int(df["year"].max())

year_range = st.sidebar.slider(
    "Select Year Range",
    year_min,
    year_max,
    (year_min, year_max)
)

countries = st.sidebar.multiselect(
    "Select Countries",
    options=df["country_name"].unique(),
    default=df["country_name"].unique()[:10]
)

# Filtered Data
filtered_df = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1]) &
    (df["country_name"].isin(countries))
]

# -----------------------
# KPI SECTION
# -----------------------
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Avg Inequality", f"{filtered_df['top20_bottom20_ratio'].mean():.2f}")
col2.metric("Max Inequality", f"{filtered_df['top20_bottom20_ratio'].max():.2f}")
col3.metric("Avg Dev Score", f"{filtered_df['development_score'].mean():.2f}")
col4.metric("Avg GDP", f"{filtered_df['gdp_per_capita'].mean():,.0f}")
col5.metric("Countries", filtered_df["country_name"].nunique())
col6.metric("Years", f"{year_range[0]} - {year_range[1]}")

# -----------------------
# 1. MAP (IMPORTANT)
# -----------------------
st.subheader("🌍 Global Inequality Map")

if "country_code" in filtered_df.columns:
    map_fig = px.choropleth(
        filtered_df,
        locations="country_code",
        color="top20_bottom20_ratio",
        hover_name="country_name",
        animation_frame="year",
        color_continuous_scale="Reds"
    )
    st.plotly_chart(map_fig, use_container_width=True)
else:
    st.warning("⚠️ 'country_code' column missing for map visualization")

# -----------------------
# 2. TREND LINE
# -----------------------
st.subheader("📈 Inequality Trend Over Time")

trend_df = filtered_df.groupby("year")["top20_bottom20_ratio"].mean().reset_index()

trend_fig = px.line(
    trend_df,
    x="year",
    y="top20_bottom20_ratio",
    markers=True
)

st.plotly_chart(trend_fig, use_container_width=True)

# -----------------------
# 3. TOP COUNTRIES BAR
# -----------------------
st.subheader("📊 Top 10 Countries by Inequality")

top_countries = (
    filtered_df.groupby("country_name")["top20_bottom20_ratio"]
    .mean()
    .nlargest(10)
    .reset_index()
)

bar_fig = px.bar(
    top_countries,
    x="country_name",
    y="top20_bottom20_ratio"
)

st.plotly_chart(bar_fig, use_container_width=True)

# -----------------------
# 4. SCATTER (GDP vs Inequality)
# -----------------------
st.subheader("🔵 GDP vs Inequality")

scatter_fig = px.scatter(
    filtered_df,
    x="gdp_per_capita",
    y="top20_bottom20_ratio",
    size="development_score",
    color="region" if "region" in filtered_df.columns else None,
    hover_name="country_name"
)

st.plotly_chart(scatter_fig, use_container_width=True)

# -----------------------
# 5. BOX PLOT
# -----------------------
st.subheader("📦 Inequality Distribution")

box_fig = px.box(
    filtered_df,
    y="top20_bottom20_ratio"
)

st.plotly_chart(box_fig, use_container_width=True)

# -----------------------
# 6. HEATMAP
# -----------------------
st.subheader("🔥 Correlation Heatmap")

corr_cols = ["top20_bottom20_ratio", "gdp_per_capita", "development_score"]
corr_cols = [col for col in corr_cols if col in filtered_df.columns]

if len(corr_cols) >= 2:
    corr = filtered_df[corr_cols].corr()

    heatmap_fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto"
    )

    st.plotly_chart(heatmap_fig, use_container_width=True)
else:
    st.warning("Not enough columns for correlation heatmap")