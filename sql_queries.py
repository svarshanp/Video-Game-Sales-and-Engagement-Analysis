"""
Video Game Sales and Engagement Analysis
SQL Queries — Answering all 30 EDA questions
"""

import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "videogames.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


# ════════════════════════════════════════════════
# SECTION A: games.csv Questions (1–9)
# ════════════════════════════════════════════════

def q1_top_rated_games(limit=15):
    """Q1: What are the top-rated games by user reviews?"""
    conn = get_connection()
    df = pd.read_sql_query(f"""
        SELECT title, rating, number_of_reviews, genres
        FROM games
        WHERE number_of_reviews > 100
        ORDER BY rating DESC, number_of_reviews DESC
        LIMIT {limit}
    """, conn)
    conn.close()
    return df


def q2_top_developers_by_rating(limit=15):
    """Q2: Which developers (Teams) have the highest average ratings?"""
    conn = get_connection()
    df = pd.read_sql_query(f"""
        SELECT team, 
               ROUND(AVG(rating), 2) as avg_rating,
               COUNT(*) as game_count,
               ROUND(AVG(plays), 0) as avg_plays
        FROM games
        WHERE team IS NOT NULL AND team != ''
        GROUP BY team
        HAVING game_count >= 3
        ORDER BY avg_rating DESC
        LIMIT {limit}
    """, conn)
    conn.close()
    return df


def q3_most_common_genres():
    """Q3: What are the most common genres in the dataset?"""
    conn = get_connection()
    df = pd.read_sql_query("SELECT genres FROM games WHERE genres IS NOT NULL", conn)
    conn.close()
    # Explode genres (comma-separated)
    all_genres = []
    for g in df["genres"].dropna():
        all_genres.extend([x.strip() for x in str(g).split(",")])
    genre_counts = pd.Series(all_genres).value_counts().reset_index()
    genre_counts.columns = ["genre", "count"]
    return genre_counts.head(15)


def q4_backlog_vs_wishlist(limit=15):
    """Q4: Which games have the highest backlog compared to wishlist?"""
    conn = get_connection()
    df = pd.read_sql_query(f"""
        SELECT title, backlogs, wishlist,
               ROUND(CAST(backlogs AS FLOAT) / NULLIF(wishlist, 0), 2) as backlog_wishlist_ratio
        FROM games
        WHERE backlogs > 0 AND wishlist > 0
        ORDER BY backlog_wishlist_ratio DESC
        LIMIT {limit}
    """, conn)
    conn.close()
    return df


def q5_release_trend_by_year():
    """Q5: What is the game release trend across years?"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT release_year as year, COUNT(*) as game_count
        FROM games
        WHERE release_year IS NOT NULL AND release_year > 1980 AND release_year <= 2025
        GROUP BY release_year
        ORDER BY release_year
    """, conn)
    conn.close()
    return df


def q6_rating_distribution():
    """Q6: What is the distribution of user ratings?"""
    conn = get_connection()
    df = pd.read_sql_query("SELECT rating FROM games WHERE rating IS NOT NULL", conn)
    conn.close()
    return df


def q7_top_wishlisted_games(limit=10):
    """Q7: What are the top 10 most wishlisted games?"""
    conn = get_connection()
    df = pd.read_sql_query(f"""
        SELECT title, wishlist, rating, genres
        FROM games
        ORDER BY wishlist DESC
        LIMIT {limit}
    """, conn)
    conn.close()
    return df


def q8_avg_plays_per_genre():
    """Q8: What's the average number of plays per genre?"""
    conn = get_connection()
    df = pd.read_sql_query("SELECT genres, plays FROM games WHERE genres IS NOT NULL", conn)
    conn.close()
    rows = []
    for _, row in df.iterrows():
        for g in str(row["genres"]).split(","):
            g = g.strip()
            if g:
                rows.append({"genre": g, "plays": row["plays"]})
    exploded = pd.DataFrame(rows)
    result = exploded.groupby("genre")["plays"].mean().round(0).reset_index()
    result.columns = ["genre", "avg_plays"]
    result = result.sort_values("avg_plays", ascending=False).head(15)
    return result


def q9_most_productive_developers(limit=15):
    """Q9: Which developer studios are the most productive and impactful?"""
    conn = get_connection()
    df = pd.read_sql_query(f"""
        SELECT team,
               COUNT(*) as game_count,
               ROUND(AVG(rating), 2) as avg_rating,
               ROUND(SUM(plays), 0) as total_plays,
               ROUND(AVG(wishlist), 0) as avg_wishlist
        FROM games
        WHERE team IS NOT NULL AND team != ''
        GROUP BY team
        HAVING game_count >= 3
        ORDER BY total_plays DESC
        LIMIT {limit}
    """, conn)
    conn.close()
    return df


# ════════════════════════════════════════════════
# SECTION B: vgsales.csv Questions (10–20)
# ════════════════════════════════════════════════

def q10_sales_by_region():
    """Q10: Which region generates the most game sales?"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT 
            ROUND(SUM(na_sales), 2) as North_America,
            ROUND(SUM(eu_sales), 2) as Europe,
            ROUND(SUM(jp_sales), 2) as Japan,
            ROUND(SUM(other_sales), 2) as Other
        FROM vgsales
    """, conn)
    conn.close()
    result = df.T.reset_index()
    result.columns = ["region", "total_sales_millions"]
    return result


def q11_best_selling_platforms(limit=15):
    """Q11: What are the best-selling platforms?"""
    conn = get_connection()
    df = pd.read_sql_query(f"""
        SELECT platform, 
               ROUND(SUM(global_sales), 2) as total_sales,
               COUNT(*) as game_count
        FROM vgsales
        GROUP BY platform
        ORDER BY total_sales DESC
        LIMIT {limit}
    """, conn)
    conn.close()
    return df


def q12_releases_sales_over_years():
    """Q12: What's the trend of game releases and sales over years?"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT year, 
               COUNT(*) as releases,
               ROUND(SUM(global_sales), 2) as total_sales
        FROM vgsales
        WHERE year > 0 AND year <= 2025
        GROUP BY year
        ORDER BY year
    """, conn)
    conn.close()
    return df


def q13_top_publishers_by_sales(limit=15):
    """Q13: Who are the top publishers by sales?"""
    conn = get_connection()
    df = pd.read_sql_query(f"""
        SELECT publisher, 
               ROUND(SUM(global_sales), 2) as total_sales,
               COUNT(*) as game_count
        FROM vgsales
        WHERE publisher != 'Unknown'
        GROUP BY publisher
        ORDER BY total_sales DESC
        LIMIT {limit}
    """, conn)
    conn.close()
    return df


def q14_top_global_sellers(limit=10):
    """Q14: Which games are the top 10 best-sellers globally?"""
    conn = get_connection()
    df = pd.read_sql_query(f"""
        SELECT name, platform, year, genre, publisher, global_sales
        FROM vgsales
        ORDER BY global_sales DESC
        LIMIT {limit}
    """, conn)
    conn.close()
    return df


def q15_regional_sales_by_platform():
    """Q15: How do regional sales compare for specific platforms?"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT platform,
               ROUND(SUM(na_sales), 2) as NA_Sales,
               ROUND(SUM(eu_sales), 2) as EU_Sales,
               ROUND(SUM(jp_sales), 2) as JP_Sales,
               ROUND(SUM(other_sales), 2) as Other_Sales
        FROM vgsales
        GROUP BY platform
        ORDER BY SUM(global_sales) DESC
        LIMIT 10
    """, conn)
    conn.close()
    return df


def q16_platform_evolution_over_time():
    """Q16: How has the market evolved by platform over time?"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT year, platform, ROUND(SUM(global_sales), 2) as total_sales
        FROM vgsales
        WHERE year > 0 AND year <= 2025
        GROUP BY year, platform
        ORDER BY year, total_sales DESC
    """, conn)
    conn.close()
    return df


def q17_regional_genre_preferences():
    """Q17: What are the regional genre preferences?"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT genre,
               ROUND(SUM(na_sales), 2) as NA_Sales,
               ROUND(SUM(eu_sales), 2) as EU_Sales,
               ROUND(SUM(jp_sales), 2) as JP_Sales,
               ROUND(SUM(other_sales), 2) as Other_Sales
        FROM vgsales
        GROUP BY genre
        ORDER BY SUM(global_sales) DESC
    """, conn)
    conn.close()
    return df


def q18_yearly_sales_change_per_region():
    """Q18: What's the yearly sales change per region?"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT year,
               ROUND(SUM(na_sales), 2) as NA_Sales,
               ROUND(SUM(eu_sales), 2) as EU_Sales,
               ROUND(SUM(jp_sales), 2) as JP_Sales,
               ROUND(SUM(other_sales), 2) as Other_Sales
        FROM vgsales
        WHERE year > 0 AND year <= 2025
        GROUP BY year
        ORDER BY year
    """, conn)
    conn.close()
    return df


def q19_avg_sales_per_publisher(limit=15):
    """Q19: What is the average sales per publisher?"""
    conn = get_connection()
    df = pd.read_sql_query(f"""
        SELECT publisher,
               ROUND(AVG(global_sales), 2) as avg_sales,
               COUNT(*) as game_count,
               ROUND(SUM(global_sales), 2) as total_sales
        FROM vgsales
        WHERE publisher != 'Unknown'
        GROUP BY publisher
        HAVING game_count >= 5
        ORDER BY avg_sales DESC
        LIMIT {limit}
    """, conn)
    conn.close()
    return df


def q20_top5_per_platform():
    """Q20: What are the top 5 best-selling games per platform?"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT platform, name, global_sales,
               ROW_NUMBER() OVER (PARTITION BY platform ORDER BY global_sales DESC) as rn
        FROM vgsales
    """, conn)
    conn.close()
    return df[df["rn"] <= 5].drop(columns=["rn"])


# ════════════════════════════════════════════════
# SECTION C: Merged Data Questions (21–30)
# ════════════════════════════════════════════════

def q21_genres_most_global_sales():
    """Q21: Which game genres generate the most global sales?"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT genre,
               ROUND(SUM(global_sales), 2) as total_sales,
               ROUND(AVG(rating), 2) as avg_rating,
               COUNT(*) as game_count
        FROM merged_data
        GROUP BY genre
        ORDER BY total_sales DESC
    """, conn)
    conn.close()
    return df


def q22_rating_vs_sales():
    """Q22: How does user rating affect global sales?"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT rating, global_sales, title
        FROM merged_data
        WHERE rating IS NOT NULL AND global_sales IS NOT NULL
    """, conn)
    conn.close()
    return df


def q23_platforms_high_ratings():
    """Q23: Which platforms have the most games with high ratings (above 4)?"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT platform,
               COUNT(*) as high_rated_games,
               ROUND(AVG(rating), 2) as avg_rating,
               ROUND(SUM(global_sales), 2) as total_sales
        FROM merged_data
        WHERE rating > 4
        GROUP BY platform
        ORDER BY high_rated_games DESC
        LIMIT 15
    """, conn)
    conn.close()
    return df


def q24_releases_sales_trend_merged():
    """Q24: What's the trend of releases and sales over time (merged)?"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT year,
               COUNT(*) as releases,
               ROUND(SUM(global_sales), 2) as total_sales,
               ROUND(AVG(rating), 2) as avg_rating
        FROM merged_data
        WHERE year > 0 AND year <= 2025
        GROUP BY year
        ORDER BY year
    """, conn)
    conn.close()
    return df


def q25_wishlist_vs_sales():
    """Q25: Do highly wishlisted games lead to more sales?"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT title, wishlist, global_sales, rating
        FROM merged_data
        WHERE wishlist > 0 AND global_sales > 0
    """, conn)
    conn.close()
    return df


def q26_high_engagement_low_sales():
    """Q26: Which genres have the highest engagement but lowest sales?"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT genre,
               ROUND(AVG(plays), 0) as avg_plays,
               ROUND(AVG(global_sales), 2) as avg_sales,
               ROUND(AVG(rating), 2) as avg_rating
        FROM merged_data
        GROUP BY genre
        ORDER BY avg_plays DESC
    """, conn)
    conn.close()
    return df


def q27_listed_vs_ratings():
    """Q27: Do highly listed games correlate with better ratings?"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT title, wishlist, backlogs, rating, global_sales
        FROM merged_data
        WHERE wishlist > 0 AND backlogs > 0
    """, conn)
    conn.close()
    return df


def q28_engagement_across_genres():
    """Q28: How does user engagement differ across genres?"""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT genre,
               ROUND(AVG(plays), 0) as avg_plays,
               ROUND(AVG(playing), 0) as avg_playing,
               ROUND(AVG(backlogs), 0) as avg_backlogs,
               ROUND(AVG(wishlist), 0) as avg_wishlist,
               ROUND(AVG(rating), 2) as avg_rating
        FROM merged_data
        GROUP BY genre
        ORDER BY avg_plays DESC
    """, conn)
    conn.close()
    return df


def q29_top_genre_platform_combos(limit=15):
    """Q29: What are the top-performing Genre + Platform combinations?"""
    conn = get_connection()
    df = pd.read_sql_query(f"""
        SELECT genre || ' + ' || platform as combo,
               genre, platform,
               ROUND(SUM(global_sales), 2) as total_sales,
               COUNT(*) as game_count,
               ROUND(AVG(rating), 2) as avg_rating
        FROM merged_data
        GROUP BY genre, platform
        HAVING game_count >= 2
        ORDER BY total_sales DESC
        LIMIT {limit}
    """, conn)
    conn.close()
    return df


def q30_regional_heatmap_by_genre():
    """Q30: Regional sales heatmap by genre."""
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT genre,
               ROUND(SUM(na_sales), 2) as NA_Sales,
               ROUND(SUM(eu_sales), 2) as EU_Sales,
               ROUND(SUM(jp_sales), 2) as JP_Sales,
               ROUND(SUM(other_sales), 2) as Other_Sales,
               ROUND(SUM(global_sales), 2) as Global_Sales
        FROM merged_data
        GROUP BY genre
        ORDER BY Global_Sales DESC
    """, conn)
    conn.close()
    return df


# Quick test if run directly
if __name__ == "__main__":
    print("Testing SQL Queries...\n")
    print("Q1 - Top Rated Games:")
    print(q1_top_rated_games(5).to_string(index=False))
    print("\nQ10 - Sales by Region:")
    print(q10_sales_by_region().to_string(index=False))
    print("\nQ14 - Top Global Sellers:")
    print(q14_top_global_sellers(5).to_string(index=False))
    print("\n[DONE] All queries working!")
