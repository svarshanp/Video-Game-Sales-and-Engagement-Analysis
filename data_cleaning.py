"""
Video Game Sales and Engagement Analysis
Step 1: Data Cleaning & Preprocessing
"""

import pandas as pd
import numpy as np
import ast
import re
import os
import sqlite3

# ──────────────────────────────────────────────
# 1. LOAD RAW DATA
# ──────────────────────────────────────────────

print("=" * 60)
print("  VIDEO GAME DATA CLEANING PIPELINE")
print("=" * 60)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("\n[1/8] Loading raw datasets...")
games_df = pd.read_csv(os.path.join(BASE_DIR, "games.csv"))
vgsales_df = pd.read_csv(os.path.join(BASE_DIR, "vgsales.csv"))

print(f"  games.csv   : {games_df.shape[0]} rows, {games_df.shape[1]} columns")
print(f"  vgsales.csv : {vgsales_df.shape[0]} rows, {vgsales_df.shape[1]} columns")

# ──────────────────────────────────────────────
# 2. CLEAN games.csv
# ──────────────────────────────────────────────

print("\n[2/8] Cleaning games.csv...")

# Drop the unnamed index column if present
if "Unnamed: 0" in games_df.columns:
    games_df.drop(columns=["Unnamed: 0"], inplace=True)

# Remove exact duplicates
before = len(games_df)
games_df.drop_duplicates(subset=["Title"], keep="first", inplace=True)
print(f"  Removed {before - len(games_df)} duplicate titles")

# ── Parse numeric columns that have 'K' suffix (e.g., "17K" → 17000) ──
def parse_k_values(val):
    """Convert values like '17K', '3.8K' to numeric."""
    if pd.isna(val):
        return np.nan
    val = str(val).strip()
    if val.upper().endswith("K"):
        try:
            return float(val[:-1]) * 1000
        except ValueError:
            return np.nan
    try:
        return float(val.replace(",", ""))
    except ValueError:
        return np.nan

for col in ["Times Listed", "Number of Reviews", "Plays", "Playing", "Backlogs", "Wishlist"]:
    if col in games_df.columns:
        games_df[col] = games_df[col].apply(parse_k_values)

print("  Converted K-suffix values to numbers (Plays, Wishlist, etc.)")

# ── Clean Rating column ──
games_df["Rating"] = pd.to_numeric(games_df["Rating"], errors="coerce")

# ── Parse Release Date ──
games_df["Release Date"] = pd.to_datetime(games_df["Release Date"], format="mixed", errors="coerce")
games_df["Release_Year"] = games_df["Release Date"].dt.year

print("  Parsed dates, ratings, and numeric fields")

# ── Clean Genres — parse the string list ──
def parse_genres(val):
    """Parse genre strings like \"['Adventure', 'RPG']\" into clean comma-separated string."""
    if pd.isna(val):
        return np.nan
    try:
        genres = ast.literal_eval(val)
        if isinstance(genres, list):
            return ", ".join([g.strip() for g in genres])
    except (ValueError, SyntaxError):
        pass
    return str(val).strip()

games_df["Genres"] = games_df["Genres"].apply(parse_genres)
print("  Parsed genre lists into clean strings")

# ── Clean Team (Developer) column ──
def parse_team(val):
    """Parse team strings like \"['FromSoftware', 'Bandai']\" into clean string."""
    if pd.isna(val):
        return np.nan
    try:
        teams = ast.literal_eval(val)
        if isinstance(teams, list):
            return ", ".join([t.strip() for t in teams])
    except (ValueError, SyntaxError):
        pass
    return str(val).strip()

games_df["Team"] = games_df["Team"].apply(parse_team)
print("  Parsed developer team names")

# ── Handle missing values ──
games_df["Rating"].fillna(games_df["Rating"].median(), inplace=True)

numeric_cols_games = ["Plays", "Playing", "Backlogs", "Wishlist", "Times Listed", "Number of Reviews"]
for col in numeric_cols_games:
    if col in games_df.columns:
        games_df[col].fillna(0, inplace=True)

print("  Handled missing values (median for rating, 0 for counts)")

# ── Reset index ──
games_df.reset_index(drop=True, inplace=True)
games_df.index.name = "game_id"
games_df.reset_index(inplace=True)


# ──────────────────────────────────────────────
# 3. CLEAN vgsales.csv
# ──────────────────────────────────────────────

print("\n[3/8] Cleaning vgsales.csv...")

# Remove exact duplicates
before = len(vgsales_df)
vgsales_df.drop_duplicates(inplace=True)
print(f"  Removed {before - len(vgsales_df)} exact duplicate rows")

# ── Clean Year ──
vgsales_df["Year"] = pd.to_numeric(vgsales_df["Year"], errors="coerce")

# ── Handle missing values ──
vgsales_df["Year"].fillna(0, inplace=True)
vgsales_df["Year"] = vgsales_df["Year"].astype(int)

vgsales_df["Publisher"].fillna("Unknown", inplace=True)
vgsales_df["Name"].fillna("Unknown", inplace=True)

# Fill missing sales with 0
sales_cols = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]
for col in sales_cols:
    vgsales_df[col].fillna(0, inplace=True)

print("  Handled missing values (0 for year/sales, 'Unknown' for text)")

# ── Normalize text fields ──
vgsales_df["Name"] = vgsales_df["Name"].str.strip()
vgsales_df["Platform"] = vgsales_df["Platform"].str.strip()
vgsales_df["Genre"] = vgsales_df["Genre"].str.strip()
vgsales_df["Publisher"] = vgsales_df["Publisher"].str.strip()

print("  Normalized text fields (trimmed whitespace)")

# ── Reset index ──
vgsales_df.reset_index(drop=True, inplace=True)
vgsales_df.index.name = "sale_id"
vgsales_df.reset_index(inplace=True)

# ──────────────────────────────────────────────
# 4. CREATE MERGED DATASET
# ──────────────────────────────────────────────

print("\n[4/8] Merging datasets...")

# Merge on game name (Title from games, Name from vgsales)
merged_df = pd.merge(
    games_df,
    vgsales_df,
    left_on="Title",
    right_on="Name",
    how="inner",
    suffixes=("_engagement", "_sales")
)

print(f"  Merged dataset: {merged_df.shape[0]} matching games found")

# ──────────────────────────────────────────────
# 5. SAVE CLEANED DATA
# ──────────────────────────────────────────────

print("\n[5/8] Saving cleaned CSVs...")

cleaned_dir = os.path.join(BASE_DIR, "cleaned_data")
os.makedirs(cleaned_dir, exist_ok=True)

games_df.to_csv(os.path.join(cleaned_dir, "games_cleaned.csv"), index=False)
vgsales_df.to_csv(os.path.join(cleaned_dir, "vgsales_cleaned.csv"), index=False)
merged_df.to_csv(os.path.join(cleaned_dir, "merged_data.csv"), index=False)

print(f"  Saved to {cleaned_dir}/")

# ──────────────────────────────────────────────
# 6. CREATE SQLITE DATABASE
# ──────────────────────────────────────────────

print("\n[6/8] Creating SQLite database...")

db_path = os.path.join(BASE_DIR, "videogames.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop tables if they exist
cursor.execute("DROP TABLE IF EXISTS merged_data")
cursor.execute("DROP TABLE IF EXISTS games")
cursor.execute("DROP TABLE IF EXISTS vgsales")

# Create games table
cursor.execute("""
CREATE TABLE games (
    game_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    release_date TEXT,
    release_year INTEGER,
    team TEXT,
    rating REAL,
    times_listed REAL,
    number_of_reviews REAL,
    genres TEXT,
    summary TEXT,
    reviews TEXT,
    plays REAL,
    playing REAL,
    backlogs REAL,
    wishlist REAL
)
""")

# Create vgsales table
cursor.execute("""
CREATE TABLE vgsales (
    sale_id INTEGER PRIMARY KEY,
    rank INTEGER,
    name TEXT NOT NULL,
    platform TEXT,
    year INTEGER,
    genre TEXT,
    publisher TEXT,
    na_sales REAL,
    eu_sales REAL,
    jp_sales REAL,
    other_sales REAL,
    global_sales REAL
)
""")

# Create merged_data table
cursor.execute("""
CREATE TABLE merged_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    release_year INTEGER,
    team TEXT,
    rating REAL,
    genres TEXT,
    plays REAL,
    playing REAL,
    backlogs REAL,
    wishlist REAL,
    platform TEXT,
    year INTEGER,
    genre TEXT,
    publisher TEXT,
    na_sales REAL,
    eu_sales REAL,
    jp_sales REAL,
    other_sales REAL,
    global_sales REAL
)
""")

conn.commit()
print("  Created tables: games, vgsales, merged_data")

# ──────────────────────────────────────────────
# 7. LOAD DATA INTO DATABASE
# ──────────────────────────────────────────────

print("\n[7/8] Loading data into SQLite...")

# Insert games data
games_db = games_df[["game_id", "Title", "Release Date", "Release_Year", "Team",
                      "Rating", "Times Listed", "Number of Reviews", "Genres",
                      "Summary", "Reviews", "Plays", "Playing", "Backlogs", "Wishlist"]].copy()
games_db.columns = ["game_id", "title", "release_date", "release_year", "team",
                     "rating", "times_listed", "number_of_reviews", "genres",
                     "summary", "reviews", "plays", "playing", "backlogs", "wishlist"]
games_db["release_date"] = games_db["release_date"].astype(str)
games_db.to_sql("games", conn, if_exists="replace", index=False)

# Insert vgsales data
vgsales_db = vgsales_df[["sale_id", "Rank", "Name", "Platform", "Year", "Genre",
                          "Publisher", "NA_Sales", "EU_Sales", "JP_Sales",
                          "Other_Sales", "Global_Sales"]].copy()
vgsales_db.columns = ["sale_id", "rank", "name", "platform", "year", "genre",
                       "publisher", "na_sales", "eu_sales", "jp_sales",
                       "other_sales", "global_sales"]
vgsales_db.to_sql("vgsales", conn, if_exists="replace", index=False)

# Insert merged data
merged_db = merged_df[["Title", "Release_Year", "Team", "Rating", "Genres",
                        "Plays", "Playing", "Backlogs", "Wishlist",
                        "Platform", "Year", "Genre", "Publisher",
                        "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].copy()
merged_db.columns = ["title", "release_year", "team", "rating", "genres",
                      "plays", "playing", "backlogs", "wishlist",
                      "platform", "year", "genre", "publisher",
                      "na_sales", "eu_sales", "jp_sales", "other_sales", "global_sales"]
merged_db.to_sql("merged_data", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print(f"  Database saved: {db_path}")

# ──────────────────────────────────────────────
# 8. SUMMARY
# ──────────────────────────────────────────────

print("\n[8/8] Cleaning Summary:")
print("=" * 60)
print(f"  games_cleaned.csv     : {len(games_df)} rows")
print(f"  vgsales_cleaned.csv   : {len(vgsales_df)} rows")
print(f"  merged_data.csv       : {len(merged_df)} rows")
print(f"  SQLite DB             : videogames.db")
print("=" * 60)
print("\n[DONE] Data cleaning complete! Run 'streamlit run app.py' for the dashboard.")
