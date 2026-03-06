import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("combined_happiness_data.csv")

st.set_page_config(page_title="World Happiness Report Explorer", layout="wide")
st.title("🌍 World Happiness Report Explorer")

# Sidebar filters
years = sorted(df["Year"].unique())
selected_year = st.sidebar.selectbox("Select Year", years)
df_year = df[df["Year"] == selected_year]

regions = df_year["Country or region"].unique()
selected_country_or_region = st.sidebar.multiselect(
    "Select Country/Region (optional)", options=regions, default=[]
)

if selected_country_or_region:
    df_year = df_year[df_year["Country or region"].isin(selected_country_or_region)]

# Show rankings
df_ranked = df_year.sort_values(by="Score", ascending=False)

st.subheader(f"Happiness Rankings ({selected_year})")
st.dataframe(df_ranked[["Country or region", "Score"]].reset_index(drop=True))

# Top and bottom N countries
col1, col2 = st.columns(2)

with col1:
    N_top = st.slider("Top N Happiest Countries", min_value=1, max_value=20, value=10)
    st.write(df_ranked.head(N_top)[["Country or region", "Score"]])

with col2:
    N_bottom = st.slider("Bottom N Countries", min_value=1, max_value=20, value=10)
    st.write(df_ranked.tail(N_bottom)[["Country or region", "Score"]])

# Correlation plot
st.subheader("📊 Correlation with Happiness Score")

numerical_cols = [
    "GDP per capita",
    "Social support",
    "Healthy life expectancy",
    "Freedom to make life choices",
    "Generosity",
    "Perceptions of corruption"
]

corr_df = df_year[numerical_cols + ["Score"]].corr()[["Score"]].drop("Score")
corr_df = corr_df.rename(columns={"Score": "Correlation with Score"}).reset_index()

fig = px.bar(
    corr_df,
    x="Correlation with Score",
    y="index",
    orientation="h",
    title=f"Correlation of Components with Happiness Score ({selected_year})",
    labels={"index": "Component"},
    color="Correlation with Score",
    color_continuous_scale="Blues",
    height=400
)

st.plotly_chart(fig, use_container_width=True)