
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Netflix Content Type Analysis", page_icon="🎬", layout="wide")

st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #f3fff8, #e1f5ec, #fbfffd);}
h1, h2, h3 {color: #286b53;}
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.9);
    border: 1px solid #cce9da;
    padding: 18px;
    border-radius: 16px;
}
.stButton button, .stDownloadButton button {border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

data_path = Path(__file__).parent / "Dataset.csv"

try:
    df = pd.read_csv(data_path)
except FileNotFoundError:
    st.error("Dataset.csv was not found. Place it in the same folder as app.py.")
    st.stop()

required_columns = {"show_id", "title", "type"}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    st.error("Dataset is missing required columns: " + ", ".join(sorted(missing_columns)))
    st.stop()

df["type"] = df["type"].fillna("Unknown").astype(str).str.strip()

if "release_year" in df.columns:
    df["release_year"] = pd.to_numeric(
        df["release_year"], errors="coerce"
    ).astype("Int64")

st.title("🎬 Netflix Content Type Analysis")
st.caption("Auspify Technologies | Data Analysis Using Python")
st.markdown("---")

st.sidebar.header("🔎 Content Filters")

content_types = sorted(df["type"].unique().tolist())
selected_types = st.sidebar.multiselect(
    "Select Content Type",
    options=content_types,
    default=content_types
)

filtered = df[df["type"].isin(selected_types)].copy()

if "release_year" in filtered.columns:
    available_years = filtered["release_year"].dropna()
    if not available_years.empty:
        min_year = int(available_years.min())
        max_year = int(available_years.max())
        if min_year < max_year:
            year_range = st.sidebar.slider(
                "Release Year Range",
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year),
                key="task2_year_range"
            )
            filtered = filtered[
                filtered["release_year"].between(year_range[0], year_range[1])
            ]

if "rating" in filtered.columns:
    ratings = sorted(filtered["rating"].dropna().astype(str).unique().tolist())
    selected_ratings = st.sidebar.multiselect(
        "Select Rating",
        options=ratings,
        default=ratings
    )
    filtered = filtered[
        filtered["rating"].isna()
        | filtered["rating"].astype(str).isin(selected_ratings)
    ]

st.sidebar.caption("Filters update the metrics, charts, and table.")

total_titles = len(filtered)
movie_count = int((filtered["type"] == "Movie").sum())
tv_count = int((filtered["type"] == "TV Show").sum())
movie_share = movie_count / total_titles * 100 if total_titles else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Titles", f"{total_titles:,}")
c2.metric("Movies", f"{movie_count:,}")
c3.metric("TV Shows", f"{tv_count:,}")
c4.metric("Movie Share", f"{movie_share:.1f}%")

st.markdown("---")
st.subheader("📊 Movies vs TV Shows")

type_summary = (
    filtered["type"].value_counts()
    .rename_axis("Content Type").reset_index(name="Titles")
)

left, right = st.columns(2)

with left:
    bar_chart = px.bar(
        type_summary,
        x="Content Type",
        y="Titles",
        text="Titles",
        color="Content Type",
        color_discrete_map={
            "Movie": "#72b99a",
            "TV Show": "#b2a0dc",
            "Unknown": "#c9d7d0"
        },
        title="Number of Titles by Content Type"
    )
    bar_chart.update_traces(textposition="outside")
    bar_chart.update_layout(
        template="plotly_white",
        showlegend=False,
        margin=dict(l=10, r=20, t=55, b=10)
    )
    st.plotly_chart(bar_chart, width="stretch", key="task2_content_bar_chart")

with right:
    pie_chart = px.pie(
        type_summary,
        names="Content Type",
        values="Titles",
        hole=0.45,
        color="Content Type",
        color_discrete_map={
            "Movie": "#72b99a",
            "TV Show": "#b2a0dc",
            "Unknown": "#c9d7d0"
        },
        title="Content Type Percentage"
    )
    pie_chart.update_layout(template="plotly_white")
    st.plotly_chart(pie_chart, width="stretch", key="task2_content_pie_chart")

if "release_year" in filtered.columns:
    st.markdown("---")
    st.subheader("📈 Content Released Over the Years")

    year_type = (
        filtered.dropna(subset=["release_year"])
        .groupby(["release_year", "type"])
        .size().reset_index(name="Titles")
    )

    if not year_type.empty:
        year_chart = px.line(
            year_type,
            x="release_year",
            y="Titles",
            color="type",
            markers=True,
            color_discrete_map={
                "Movie": "#72b99a",
                "TV Show": "#b2a0dc",
                "Unknown": "#c9d7d0"
            },
            labels={
                "release_year": "Release Year",
                "Titles": "Number of Titles",
                "type": "Content Type"
            },
            title="Release-Year Trend by Content Type"
        )
        year_chart.update_layout(
            template="plotly_white",
            hovermode="x unified"
        )
        st.plotly_chart(year_chart, width="stretch", key="task2_release_year_chart")

st.markdown("---")
st.subheader("📋 Explore Netflix Titles")

search_text = st.text_input(
    "Search by title",
    placeholder="Enter a title...",
    key="task2_title_search"
)

if search_text.strip():
    filtered = filtered[
        filtered["title"].astype(str).str.contains(
            search_text.strip(), case=False, na=False
        )
    ]

st.write(f"**Matching titles:** {len(filtered):,}")

preview_columns = [
    column for column in [
        "show_id", "title", "type", "release_year",
        "country", "rating", "duration", "listed_in"
    ] if column in filtered.columns
]

st.dataframe(
    filtered[preview_columns].head(200),
    width="stretch",
    hide_index=True
)

st.caption("The preview displays up to 200 matching titles.")

st.download_button(
    "📥 Download Filtered Titles CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="netflix_content_analysis.csv",
    mime="text/csv",
    key="task2_download_filtered"
)

st.markdown("---")
st.caption("Netflix Content Analysis | Python • Pandas • Plotly • Streamlit")

