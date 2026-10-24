import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Netflix Content Analytics",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #E8F3FF, #F8FBFF, #E7F7FA);
}
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2rem; }
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #C9E1FA;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 12px #467DB515;
}
h1, h2, h3 { color: #356A9A !important; }
.stButton > button, .stDownloadButton > button {
    background: #467DB5;
    color: white;
    border-radius: 10px;
    border: none;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: #356A9A;
    color: white;
}
</style>
""", unsafe_allow_html=True)

file = Path(__file__).parent / "Dataset.csv"
df = pd.read_csv(file)

st.title("🎬 Netflix Content Analytics")
st.caption("A Data Analysis Project | Auspify Technologies Internship")

counts = df["type"].value_counts()
total = len(df)
movies = int(counts.get("Movie", 0))
shows = int(counts.get("TV Show", 0))

c1, c2, c3 = st.columns(3)
c1.metric("Total Titles", f"{total:,}")
c2.metric("Movies", f"{movies:,}", f"{movies/total*100:.1f}% of titles")
c3.metric("TV Shows", f"{shows:,}", f"{shows/total*100:.1f}% of titles")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Content Type Distribution")
    bar = px.bar(
        counts.rename_axis("Content Type").reset_index(name="Titles"),
        x="Content Type",
        y="Titles",
        text="Titles",
        color="Content Type",
        title="Movies vs TV Shows"
    )
    bar.update_layout(showlegend=False)
    st.plotly_chart(bar, use_container_width=True)

with right:
    st.subheader("Content Share")
    pie = px.pie(
        counts.rename_axis("Content Type").reset_index(name="Titles"),
        names="Content Type",
        values="Titles",
        hole=0.4,
        title="Percentage of Total Titles"
    )
    st.plotly_chart(pie, use_container_width=True)

st.subheader("Explore the Dataset")
selected_type = st.selectbox(
    "Filter by content type",
    ["All"] + sorted(df["type"].dropna().unique().tolist())
)

filtered = df if selected_type == "All" else df[df["type"] == selected_type]
st.write(f"Showing {len(filtered):,} titles")
st.dataframe(filtered.head(100), use_container_width=True)

st.download_button(
    "Download filtered data as CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="netflix_filtered.csv",
    mime="text/csv"
)

st.caption("Dataset: Netflix titles | Built with Python, Pandas, Streamlit and Plotly")
