# 🎮 Video Game Sales and Engagement Analysis

## Project Overview
This project analyzes and visualizes video game sales and engagement data to uncover trends in game popularity, user behavior, and platform performance. By merging sales data with engagement metrics, we provide actionable insights for game developers, marketers, and publishers.

**Domain:** Gaming and Entertainment Analytics  
**Skills:** Python, SQL, Streamlit, Data Cleaning, EDA, Data Visualization

---

## 📁 Project Structure

```
├── games.csv                    # Raw engagement data (3,484 games)
├── vgsales.csv                  # Raw sales data (16,598 entries)
├── data_cleaning.py             # Data cleaning & preprocessing pipeline
├── sql_queries.py               # All 30 EDA queries (Python + SQL)
├── schema_and_queries.sql       # SQL schema & standalone queries
├── app.py                       # Streamlit interactive dashboard
├── requirements.txt             # Python dependencies
├── videogames.db                # SQLite database (generated)
├── cleaned_data/                # Cleaned CSVs (generated)
│   ├── games_cleaned.csv
│   ├── vgsales_cleaned.csv
│   └── merged_data.csv
└── README.md                    # This file
```

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Data Cleaning Pipeline
```bash
python data_cleaning.py
```
This will:
- Clean both CSV datasets (duplicates, missing values, format normalization)
- Create a merged dataset
- Generate a SQLite database (`videogames.db`)
- Save cleaned CSVs to `cleaned_data/`

### 3. Launch the Dashboard
```bash
streamlit run app.py
```

---

## 📊 Datasets

### Dataset 1: `games.csv` (Game Engagement Data)
| Column | Description |
|--------|-------------|
| Title | Game name |
| Release Date | Date of release |
| Team | Developer studio(s) |
| Rating | User review score (0-5) |
| Genres | Game categories (multiple) |
| Plays | Number of playthroughs |
| Playing | Currently playing users |
| Backlogs | Users planning to play |
| Wishlist | Users who wishlisted |
| Times Listed | Times added to lists |
| Number of Reviews | Total review count |
| Summary | Game description |
| Reviews | Sample user reviews |

### Dataset 2: `vgsales.csv` (Sales Data)
| Column | Description |
|--------|-------------|
| Rank | Sales ranking |
| Name | Game name |
| Platform | Console/device |
| Year | Release year |
| Genre | Main category |
| Publisher | Game publisher |
| NA_Sales | North America sales (millions) |
| EU_Sales | Europe sales (millions) |
| JP_Sales | Japan sales (millions) |
| Other_Sales | Other regions (millions) |
| Global_Sales | Worldwide total (millions) |

---

## 🔍 Data Cleaning Steps

1. **Duplicate Removal** — Removed duplicate titles from games.csv
2. **Numeric Parsing** — Converted K-suffix values (e.g., "17K" → 17000) for plays, wishlists, backlogs
3. **Genre/Team Parsing** — Parsed Python list strings into clean comma-separated values
4. **Date Standardization** — Parsed release dates into datetime format
5. **Missing Value Handling** — Median imputation for ratings, 0-fill for counts, "Unknown" for publishers
6. **Text Normalization** — Stripped whitespace from all categorical fields
7. **Data Merging** — Inner join on game name (Title ↔ Name)

---

## 📈 EDA Questions Answered (30 Total)

### Section A: Game Engagement (games.csv)
1. Top-rated games by user reviews
2. Developers with highest average ratings
3. Most common genres
4. Highest backlog-to-wishlist ratio games
5. Game release trend across years
6. Distribution of user ratings
7. Top 10 most wishlisted games
8. Average plays per genre
9. Most productive & impactful developer studios

### Section B: Sales Analysis (vgsales.csv)
10. Sales by region (NA vs EU vs JP vs Other)
11. Best-selling platforms
12. Releases & sales trend over years
13. Top publishers by sales
14. Top 10 global best-sellers
15. Regional sales comparison by platform
16. Market evolution by platform over time
17. Regional genre preferences
18. Yearly sales change per region
19. Average sales per publisher
20. Top 5 best-selling games per platform

### Section C: Merged Insights (Sales + Engagement)
21. Genres generating the most global sales
22. User rating impact on global sales
23. Platforms with most highly-rated games
24. Releases & sales trend (merged)
25. Wishlist correlation with sales
26. High engagement but low sales genres
27. Wishlist/backlogs correlation with ratings
28. Engagement differences across genres
29. Top-performing genre + platform combos
30. Regional sales heatmap by genre

---

## 🖥️ Dashboard Features

- **4 Interactive Tabs:** Game Engagement, Sales Analysis, Merged Insights, Data Explorer
- **KPI Cards:** Total games, global sales, average rating, platforms count
- **Interactive Filters:** Genre, platform, year range (sidebar)
- **Chart Types:** Bar, pie, scatter, line, area, treemap, heatmap
- **Dark Theme:** Premium design with gradient styling

---

## 🛠️ Technical Stack

| Technology | Purpose |
|-----------|---------|
| Python (pandas, numpy) | Data cleaning & preprocessing |
| SQLite | Database storage & queries |
| Plotly | Interactive visualizations |
| Streamlit | Web dashboard framework |
| SQL | Data querying & analysis |

---

## 📌 Key Insights

1. **North America dominates global sales**, accounting for the largest share of revenue
2. **Action and Sports genres** lead in sales volume, while **RPGs** have higher engagement
3. **Nintendo** is the top publisher by total sales across all regions
4. **Wii and PS2** are historically the best-selling platforms
5. **Higher ratings don't directly correlate with higher sales** — many niche, highly-rated games have lower sales
6. **Wishlisted games show moderate correlation with eventual sales**
7. **Japan has distinctly different genre preferences** compared to NA/EU, favoring RPGs
8. **Game releases peaked around 2008-2009** before declining

---

## 📝 License
This project is for educational purposes as part of the GUVI Data Science curriculum.
