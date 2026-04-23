"""
Video Game Sales and Engagement Analysis
Interactive Streamlit Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sqlite3

# ── Page config ──
st.set_page_config(
    page_title="🎮 Video Game Sales & Engagement Analysis",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS for premium look ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }

    .main-header h1 {
        color: white !important;
        font-weight: 700;
        font-size: 2rem;
        margin: 0;
    }

    .main-header p {
        color: rgba(255,255,255,0.85);
        font-size: 1.05rem;
        margin: 0.5rem 0 0 0;
    }

    .kpi-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1.5rem;
        border-radius: 14px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        transition: transform 0.2s ease;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .kpi-label {
        color: #a0aec0;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.3rem;
    }

    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #e2e8f0;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.3);
    }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
    }
</style>
""", unsafe_allow_html=True)

# ── Load data ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@st.cache_data
def load_data():
    """Load cleaned datasets."""
    cleaned_dir = os.path.join(BASE_DIR, "cleaned_data")

    if not os.path.exists(cleaned_dir):
        st.error("⚠️ Cleaned data not found! Please run `python data_cleaning.py` first.")
        st.stop()

    games = pd.read_csv(os.path.join(cleaned_dir, "games_cleaned.csv"))
    vgsales = pd.read_csv(os.path.join(cleaned_dir, "vgsales_cleaned.csv"))
    merged = pd.read_csv(os.path.join(cleaned_dir, "merged_data.csv"))

    return games, vgsales, merged


games_df, vgsales_df, merged_df = load_data()

# ── Color palette ──
COLORS = px.colors.sequential.Purp
PALETTE = ["#667eea", "#764ba2", "#f093fb", "#f5576c", "#4facfe",
           "#00f2fe", "#43e97b", "#fa709a", "#fee140", "#a18cd1"]

# ════════════════════════════════════════════════
# HEADER
# ════════════════════════════════════════════════

st.markdown("""
<div class="main-header">
    <h1>🎮 Video Game Sales & Engagement Analysis</h1>
    <p>Exploring trends in game popularity, user behavior, and platform performance across 16,000+ titles</p>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# KPI ROW
# ════════════════════════════════════════════════

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{len(games_df):,}</div>
        <div class="kpi-label">Games Tracked</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{vgsales_df['Global_Sales'].sum():,.0f}M</div>
        <div class="kpi-label">Global Sales (Units)</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{games_df['Rating'].mean():.2f}</div>
        <div class="kpi-label">Avg Rating</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{vgsales_df['Platform'].nunique()}</div>
        <div class="kpi-label">Platforms</div>
    </div>""", unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{len(merged_df):,}</div>
        <div class="kpi-label">Merged Records</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# SIDEBAR FILTERS
# ════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🔍 Filters")

    # Genre filter
    all_genres_raw = games_df["Genres"].dropna().str.split(",").explode().str.strip().unique()
    all_genres = sorted([g for g in all_genres_raw if g])
    selected_genres = st.multiselect("Select Genres", all_genres, default=[])

    # Platform filter  
    all_platforms = sorted(vgsales_df["Platform"].dropna().unique())
    selected_platforms = st.multiselect("Select Platforms", all_platforms, default=[])

    # Year range
    valid_years = vgsales_df[vgsales_df["Year"] > 0]["Year"]
    if len(valid_years) > 0:
        year_range = st.slider(
            "Year Range",
            int(valid_years.min()), int(valid_years.max()),
            (int(valid_years.min()), int(valid_years.max()))
        )
    else:
        year_range = (1980, 2025)

    st.markdown("---")
    st.markdown("### 📊 Project Info")
    st.markdown("""
    **Skills:** Python, SQL, Streamlit, EDA  
    **Domain:** Gaming Analytics  
    **Data:** 2 datasets merged
    """)

# Apply filters to vgsales
vgsales_filtered = vgsales_df.copy()
if selected_platforms:
    vgsales_filtered = vgsales_filtered[vgsales_filtered["Platform"].isin(selected_platforms)]
vgsales_filtered = vgsales_filtered[
    (vgsales_filtered["Year"] >= year_range[0]) & (vgsales_filtered["Year"] <= year_range[1])
]

# ════════════════════════════════════════════════
# TABS
# ════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs([
    "📁 Game Engagement (Q1-Q9)",
    "💰 Sales Analysis (Q10-Q20)",
    "🔁 Merged Insights (Q21-Q30)",
    "📋 Data Explorer"
])

# ════════════════════════════════════════════════
# TAB 1: GAME ENGAGEMENT (Q1-Q9)
# ════════════════════════════════════════════════

with tab1:
    st.markdown('<div class="section-header">📁 Game Engagement Analysis (games.csv)</div>', unsafe_allow_html=True)

    # Q1: Top Rated Games
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### 🌟 Q1: Top-Rated Games by User Reviews")
        top_rated = games_df[games_df["Number of Reviews"] > 100].nlargest(15, "Rating")
        fig = px.bar(
            top_rated, x="Rating", y="Title", orientation="h",
            color="Rating", color_continuous_scale="Purp",
            hover_data=["Number of Reviews", "Genres"]
        )
        fig.update_layout(
            height=450, yaxis=dict(autorange="reversed"),
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True, key="q1_chart")

    with col_b:
        st.markdown("#### 🧑‍🤝‍🧑 Q2: Developers with Highest Avg Rating")
        devs = games_df[games_df["Team"].notna()].groupby("Team").agg(
            avg_rating=("Rating", "mean"), game_count=("Title", "count")
        ).reset_index()
        devs = devs[devs["game_count"] >= 3].nlargest(15, "avg_rating")
        fig = px.bar(
            devs, x="avg_rating", y="Team", orientation="h",
            color="game_count", color_continuous_scale="Viridis",
            hover_data=["game_count"]
        )
        fig.update_layout(
            height=450, yaxis=dict(autorange="reversed"),
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True, key="q2_chart")

    # Q3 & Q6
    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown("#### 🧩 Q3: Most Common Genres")
        all_g = []
        for g in games_df["Genres"].dropna():
            all_g.extend([x.strip() for x in str(g).split(",")])
        genre_counts = pd.Series(all_g).value_counts().head(12).reset_index()
        genre_counts.columns = ["Genre", "Count"]
        fig = px.pie(
            genre_counts, names="Genre", values="Count",
            color_discrete_sequence=PALETTE, hole=0.4
        )
        fig.update_layout(
            height=400, template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True, key="q3_chart")

    with col_d:
        st.markdown("#### 🔎 Q6: Distribution of User Ratings")
        fig = px.histogram(
            games_df, x="Rating", nbins=20,
            color_discrete_sequence=["#667eea"],
            marginal="box"
        )
        fig.update_layout(
            height=400, template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True, key="q6_chart")

    # Q5: Release Trend
    st.markdown("#### 🗓️ Q5: Game Release Trend Across Years")
    yearly = games_df[games_df["Release_Year"].notna() & (games_df["Release_Year"] > 1980)]
    yearly_counts = yearly.groupby("Release_Year").size().reset_index(name="Count")
    fig = px.area(
        yearly_counts, x="Release_Year", y="Count",
        color_discrete_sequence=["#667eea"]
    )
    fig.update_layout(
        height=350, template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True, key="q5_chart")

    # Q4, Q7, Q8, Q9
    col_e, col_f = st.columns(2)

    with col_e:
        st.markdown("#### 🧑 Q7: Top 10 Most Wishlisted Games")
        wishlisted = games_df.nlargest(10, "Wishlist")[["Title", "Wishlist", "Rating"]]
        fig = px.bar(
            wishlisted, x="Wishlist", y="Title", orientation="h",
            color="Rating", color_continuous_scale="RdYlGn",
            text="Wishlist"
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig.update_layout(
            height=400, yaxis=dict(autorange="reversed"),
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True, key="q7_chart")

    with col_f:
        st.markdown("#### 🔬 Q8: Average Plays per Genre")
        rows = []
        for _, row in games_df.iterrows():
            if pd.notna(row["Genres"]):
                for g in str(row["Genres"]).split(","):
                    g = g.strip()
                    if g:
                        rows.append({"genre": g, "plays": row["Plays"]})
        genre_plays = pd.DataFrame(rows).groupby("genre")["plays"].mean().nlargest(12).reset_index()
        genre_plays.columns = ["Genre", "Avg Plays"]
        fig = px.bar(
            genre_plays, x="Genre", y="Avg Plays",
            color="Avg Plays", color_continuous_scale="Purp"
        )
        fig.update_layout(
            height=400, template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True, key="q8_chart")

    # Q4 Table & Q9 Table
    col_g, col_h = st.columns(2)

    with col_g:
        st.markdown("#### ⏳ Q4: Highest Backlog-to-Wishlist Ratio")
        bl = games_df[games_df["Wishlist"] > 0].copy()
        bl["Ratio"] = (bl["Backlogs"] / bl["Wishlist"]).round(2)
        st.dataframe(
            bl.nlargest(10, "Ratio")[["Title", "Backlogs", "Wishlist", "Ratio"]],
            use_container_width=True, hide_index=True
        )

    with col_h:
        st.markdown("#### 🏢 Q9: Most Productive & Impactful Studios")
        studios = games_df[games_df["Team"].notna()].groupby("Team").agg(
            Games=("Title", "count"),
            Avg_Rating=("Rating", "mean"),
            Total_Plays=("Plays", "sum")
        ).reset_index()
        studios = studios[studios["Games"] >= 3].nlargest(10, "Total_Plays")
        studios["Avg_Rating"] = studios["Avg_Rating"].round(2)
        studios["Total_Plays"] = studios["Total_Plays"].astype(int)
        st.dataframe(studios, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════
# TAB 2: SALES ANALYSIS (Q10-Q20)
# ════════════════════════════════════════════════

with tab2:
    st.markdown('<div class="section-header">💰 Sales Analysis (vgsales.csv)</div>', unsafe_allow_html=True)

    # Q10 & Q11
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### 🌍 Q10: Sales by Region")
        region_data = pd.DataFrame({
            "Region": ["North America", "Europe", "Japan", "Other"],
            "Sales (M)": [
                vgsales_filtered["NA_Sales"].sum(),
                vgsales_filtered["EU_Sales"].sum(),
                vgsales_filtered["JP_Sales"].sum(),
                vgsales_filtered["Other_Sales"].sum()
            ]
        })
        fig = px.pie(
            region_data, names="Region", values="Sales (M)",
            color_discrete_sequence=PALETTE, hole=0.45
        )
        fig.update_traces(textinfo="percent+label+value")
        fig.update_layout(
            height=400, template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True, key="q10_chart")

    with col_b:
        st.markdown("#### 🕹️ Q11: Best-Selling Platforms")
        plat_sales = vgsales_filtered.groupby("Platform")["Global_Sales"].sum().nlargest(12).reset_index()
        fig = px.bar(
            plat_sales, x="Platform", y="Global_Sales",
            color="Global_Sales", color_continuous_scale="Purp",
            text="Global_Sales"
        )
        fig.update_traces(texttemplate="%{text:.1f}M", textposition="outside")
        fig.update_layout(
            height=400, template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True, key="q11_chart")

    # Q12: Releases & Sales Over Years
    st.markdown("#### 📅 Q12: Game Releases & Sales Over Years")
    yearly_sales = vgsales_filtered[vgsales_filtered["Year"] > 0].groupby("Year").agg(
        Releases=("Name", "count"),
        Total_Sales=("Global_Sales", "sum")
    ).reset_index()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=yearly_sales["Year"], y=yearly_sales["Releases"],
               name="Releases", marker_color="rgba(102,126,234,0.6)"),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=yearly_sales["Year"], y=yearly_sales["Total_Sales"],
                   name="Total Sales (M)", line=dict(color="#f5576c", width=3)),
        secondary_y=True
    )
    fig.update_layout(
        height=400, template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    fig.update_yaxes(title_text="Number of Releases", secondary_y=False)
    fig.update_yaxes(title_text="Total Sales (M)", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True, key="q12_chart")

    # Q13 & Q14
    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown("#### 🏢 Q13: Top Publishers by Sales")
        pub_sales = vgsales_filtered[vgsales_filtered["Publisher"] != "Unknown"].groupby("Publisher")["Global_Sales"].sum().nlargest(12).reset_index()
        fig = px.treemap(
            pub_sales, path=["Publisher"], values="Global_Sales",
            color="Global_Sales", color_continuous_scale="Purp"
        )
        fig.update_layout(
            height=400, template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True, key="q13_chart")

    with col_d:
        st.markdown("#### 🔝 Q14: Top 10 Best-Sellers Globally")
        top_sellers = vgsales_filtered.nlargest(10, "Global_Sales")[
            ["Name", "Platform", "Year", "Genre", "Global_Sales"]
        ]
        fig = px.bar(
            top_sellers, x="Global_Sales", y="Name", orientation="h",
            color="Genre", color_discrete_sequence=PALETTE,
            text="Global_Sales"
        )
        fig.update_traces(texttemplate="%{text:.1f}M", textposition="outside")
        fig.update_layout(
            height=400, yaxis=dict(autorange="reversed"),
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True, key="q14_chart")

    # Q15: Regional Sales by Platform
    st.markdown("#### 🧭 Q15: Regional Sales Comparison by Platform")
    plat_regional = vgsales_filtered.groupby("Platform").agg(
        NA=("NA_Sales", "sum"), EU=("EU_Sales", "sum"),
        JP=("JP_Sales", "sum"), Other=("Other_Sales", "sum")
    ).reset_index()
    plat_regional["Total"] = plat_regional[["NA", "EU", "JP", "Other"]].sum(axis=1)
    plat_regional = plat_regional.nlargest(10, "Total").drop(columns=["Total"])
    fig = px.bar(
        plat_regional.melt(id_vars="Platform", var_name="Region", value_name="Sales"),
        x="Platform", y="Sales", color="Region", barmode="group",
        color_discrete_sequence=PALETTE
    )
    fig.update_layout(
        height=400, template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True, key="q15_chart")

    # Q17: Regional Genre Preferences
    col_e, col_f = st.columns(2)

    with col_e:
        st.markdown("#### 📍 Q17: Regional Genre Preferences")
        genre_regional = vgsales_filtered.groupby("Genre").agg(
            NA=("NA_Sales", "sum"), EU=("EU_Sales", "sum"),
            JP=("JP_Sales", "sum"), Other=("Other_Sales", "sum")
        ).reset_index()
        genre_regional_melted = genre_regional.melt(id_vars="Genre", var_name="Region", value_name="Sales")
        fig = px.bar(
            genre_regional_melted, x="Genre", y="Sales", color="Region",
            barmode="stack", color_discrete_sequence=PALETTE
        )
        fig.update_layout(
            height=400, template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True, key="q17_chart")

    with col_f:
        st.markdown("#### 🧮 Q19: Average Sales per Publisher (Top 15)")
        pub_avg = vgsales_filtered[vgsales_filtered["Publisher"] != "Unknown"].groupby("Publisher").agg(
            avg_sales=("Global_Sales", "mean"), count=("Name", "count")
        ).reset_index()
        pub_avg = pub_avg[pub_avg["count"] >= 5].nlargest(15, "avg_sales")
        fig = px.bar(
            pub_avg, x="avg_sales", y="Publisher", orientation="h",
            color="count", color_continuous_scale="Viridis",
            text="avg_sales"
        )
        fig.update_traces(texttemplate="%{text:.2f}M", textposition="outside")
        fig.update_layout(
            height=400, yaxis=dict(autorange="reversed"),
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True, key="q19_chart")

    # Q18: Yearly Sales Change per Region
    st.markdown("#### 🔄 Q18: Yearly Sales Change per Region")
    yearly_region = vgsales_filtered[vgsales_filtered["Year"] > 0].groupby("Year").agg(
        NA=("NA_Sales", "sum"), EU=("EU_Sales", "sum"),
        JP=("JP_Sales", "sum"), Other=("Other_Sales", "sum")
    ).reset_index()
    fig = px.line(
        yearly_region.melt(id_vars="Year", var_name="Region", value_name="Sales"),
        x="Year", y="Sales", color="Region",
        color_discrete_sequence=PALETTE, markers=True
    )
    fig.update_layout(
        height=400, template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True, key="q18_chart")

    # Q16 & Q20
    col_g, col_h = st.columns(2)

    with col_g:
        st.markdown("#### 📈 Q16: Market Evolution by Top 5 Platforms")
        top5_plats = vgsales_filtered.groupby("Platform")["Global_Sales"].sum().nlargest(5).index
        evo = vgsales_filtered[vgsales_filtered["Platform"].isin(top5_plats) & (vgsales_filtered["Year"] > 0)]
        evo_grouped = evo.groupby(["Year", "Platform"])["Global_Sales"].sum().reset_index()
        fig = px.line(
            evo_grouped, x="Year", y="Global_Sales", color="Platform",
            color_discrete_sequence=PALETTE, markers=True
        )
        fig.update_layout(
            height=400, template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True, key="q16_chart")

    with col_h:
        st.markdown("#### 🏆 Q20: Top 5 Best-Selling Games per Platform")
        sel_plat = st.selectbox("Choose Platform", sorted(vgsales_filtered["Platform"].unique()), key="q20_plat")
        top5_games = vgsales_filtered[vgsales_filtered["Platform"] == sel_plat].nlargest(5, "Global_Sales")
        fig = px.bar(
            top5_games, x="Global_Sales", y="Name", orientation="h",
            color="Genre", color_discrete_sequence=PALETTE,
            text="Global_Sales"
        )
        fig.update_traces(texttemplate="%{text:.1f}M", textposition="outside")
        fig.update_layout(
            height=400, yaxis=dict(autorange="reversed"),
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True, key="q20_chart")


# ════════════════════════════════════════════════
# TAB 3: MERGED INSIGHTS (Q21-Q30)
# ════════════════════════════════════════════════

with tab3:
    st.markdown('<div class="section-header">🔁 Merged Dataset Insights (Sales + Engagement)</div>', unsafe_allow_html=True)

    if len(merged_df) == 0:
        st.warning("No matching games found between the two datasets. Merged analysis unavailable.")
    else:
        # Q21 & Q22
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("#### 🎮 Q21: Genres by Global Sales (Merged)")
            genre_sales = merged_df.groupby("Genre").agg(
                Total_Sales=("Global_Sales", "sum"),
                Avg_Rating=("Rating", "mean")
            ).reset_index().sort_values("Total_Sales", ascending=False)
            fig = px.bar(
                genre_sales, x="Genre", y="Total_Sales",
                color="Avg_Rating", color_continuous_scale="RdYlGn",
                text="Total_Sales"
            )
            fig.update_traces(texttemplate="%{text:.1f}M", textposition="outside")
            fig.update_layout(
                height=400, template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True, key="q21_chart")

        with col_b:
            st.markdown("#### 🎯 Q22: Rating vs Global Sales")
            fig = px.scatter(
                merged_df, x="Rating", y="Global_Sales",
                color="Genre", size="Plays",
                hover_name="Title", color_discrete_sequence=PALETTE,
                size_max=30, opacity=0.7
            )
            fig.update_layout(
                height=400, template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True, key="q22_chart")

        # Q23 & Q25
        col_c, col_d = st.columns(2)

        with col_c:
            st.markdown("#### 🕹️ Q23: Platforms with Most Highly-Rated Games (>4)")
            high_rated = merged_df[merged_df["Rating"] > 4].groupby("Platform").agg(
                Count=("Title", "count"),
                Avg_Rating=("Rating", "mean"),
                Total_Sales=("Global_Sales", "sum")
            ).reset_index().sort_values("Count", ascending=False).head(12)
            fig = px.bar(
                high_rated, x="Platform", y="Count",
                color="Total_Sales", color_continuous_scale="Purp",
                text="Count"
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(
                height=400, template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True, key="q23_chart")

        with col_d:
            st.markdown("#### 🧍 Q25: Wishlist vs Sales")
            fig = px.scatter(
                merged_df[merged_df["Wishlist"] > 0],
                x="Wishlist", y="Global_Sales",
                color="Rating", color_continuous_scale="Viridis",
                hover_name="Title", opacity=0.7, size_max=20
            )
            fig.update_layout(
                height=400, template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True, key="q25_chart")

        # Q24: Trend over time
        st.markdown("#### 📈 Q24: Releases & Sales Trend Over Time (Merged)")
        merged_yearly = merged_df[merged_df["Year"] > 0].groupby("Year").agg(
            Releases=("Title", "count"), Sales=("Global_Sales", "sum"),
            Avg_Rating=("Rating", "mean")
        ).reset_index()

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(x=merged_yearly["Year"], y=merged_yearly["Releases"],
                   name="Releases", marker_color="rgba(102,126,234,0.6)"),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(x=merged_yearly["Year"], y=merged_yearly["Sales"],
                       name="Total Sales (M)", line=dict(color="#f5576c", width=3)),
            secondary_y=True
        )
        fig.update_layout(
            height=350, template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True, key="q24_chart")

        # Q26 & Q28
        col_e, col_f = st.columns(2)

        with col_e:
            st.markdown("#### 🎮 Q26: High Engagement vs Low Sales Genres")
            eng_sales = merged_df.groupby("Genre").agg(
                Avg_Plays=("Plays", "mean"), Avg_Sales=("Global_Sales", "mean")
            ).reset_index()
            fig = px.scatter(
                eng_sales, x="Avg_Plays", y="Avg_Sales",
                text="Genre", size="Avg_Plays",
                color="Avg_Sales", color_continuous_scale="RdYlGn"
            )
            fig.update_traces(textposition="top center")
            fig.update_layout(
                height=400, template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True, key="q26_chart")

        with col_f:
            st.markdown("#### 🏷️ Q28: Engagement Across Genres")
            eng_genres = merged_df.groupby("Genre").agg(
                Avg_Plays=("Plays", "mean"), Avg_Backlogs=("Backlogs", "mean"),
                Avg_Wishlist=("Wishlist", "mean")
            ).reset_index()
            fig = px.bar(
                eng_genres.melt(id_vars="Genre", var_name="Metric", value_name="Value"),
                x="Genre", y="Value", color="Metric", barmode="group",
                color_discrete_sequence=PALETTE
            )
            fig.update_layout(
                height=400, template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True, key="q28_chart")

        # Q27: Listed vs Ratings
        col_g, col_h = st.columns(2)

        with col_g:
            st.markdown("#### 🧠 Q27: Wishlist/Backlogs vs Ratings")
            fig = px.scatter(
                merged_df[(merged_df["Wishlist"] > 0) & (merged_df["Backlogs"] > 0)],
                x="Wishlist", y="Rating", size="Backlogs",
                color="Global_Sales", color_continuous_scale="Viridis",
                hover_name="Title", opacity=0.7
            )
            fig.update_layout(
                height=400, template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True, key="q27_chart")

        with col_h:
            st.markdown("#### 🎉 Q29: Top Genre + Platform Combos")
            combos = merged_df.groupby(["Genre", "Platform"]).agg(
                Sales=("Global_Sales", "sum"), Count=("Title", "count")
            ).reset_index()
            combos = combos[combos["Count"] >= 2].nlargest(12, "Sales")
            combos["Combo"] = combos["Genre"] + " + " + combos["Platform"]
            fig = px.bar(
                combos, x="Sales", y="Combo", orientation="h",
                color="Count", color_continuous_scale="Purp",
                text="Sales"
            )
            fig.update_traces(texttemplate="%{text:.1f}M", textposition="outside")
            fig.update_layout(
                height=400, yaxis=dict(autorange="reversed"),
                template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True, key="q29_chart")

        # Q30: Regional Heatmap
        st.markdown("#### 🌐 Q30: Regional Sales Heatmap by Genre")
        heatmap_data = merged_df.groupby("Genre").agg(
            NA=("NA_Sales", "sum"), EU=("EU_Sales", "sum"),
            JP=("JP_Sales", "sum"), Other=("Other_Sales", "sum")
        ).reset_index()
        heatmap_data = heatmap_data.set_index("Genre")

        fig = px.imshow(
            heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            color_continuous_scale="Purp",
            labels=dict(x="Region", y="Genre", color="Sales (M)"),
            text_auto=".1f"
        )
        fig.update_layout(
            height=500, template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True, key="q30_chart")


# ════════════════════════════════════════════════
# TAB 4: DATA EXPLORER
# ════════════════════════════════════════════════

with tab4:
    st.markdown('<div class="section-header">📋 Raw Data Explorer</div>', unsafe_allow_html=True)

    dataset_choice = st.radio(
        "Select Dataset", ["Games (Engagement)", "VG Sales", "Merged Data"],
        horizontal=True
    )

    if dataset_choice == "Games (Engagement)":
        st.dataframe(games_df.head(100), use_container_width=True, hide_index=True)
        st.caption(f"Showing 100 of {len(games_df)} rows")
    elif dataset_choice == "VG Sales":
        st.dataframe(vgsales_filtered.head(100), use_container_width=True, hide_index=True)
        st.caption(f"Showing 100 of {len(vgsales_filtered)} rows (filtered)")
    else:
        st.dataframe(merged_df.head(100), use_container_width=True, hide_index=True)
        st.caption(f"Showing 100 of {len(merged_df)} rows")

    # Summary statistics
    st.markdown("#### 📊 Summary Statistics")
    if dataset_choice == "Games (Engagement)":
        st.dataframe(games_df.describe().round(2), use_container_width=True)
    elif dataset_choice == "VG Sales":
        st.dataframe(vgsales_filtered.describe().round(2), use_container_width=True)
    else:
        st.dataframe(merged_df.describe().round(2), use_container_width=True)


# ── Footer ──
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#718096; font-size:0.85rem;'>"
    "🎮 Video Game Sales & Engagement Analysis | Built with Python, SQL & Streamlit"
    "</div>",
    unsafe_allow_html=True
)
