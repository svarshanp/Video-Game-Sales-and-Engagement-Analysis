-- ╔═══════════════════════════════════════════════════════╗
-- ║  VIDEO GAME SALES AND ENGAGEMENT ANALYSIS            ║
-- ║  SQL Database Schema & Sample Queries                ║
-- ╚═══════════════════════════════════════════════════════╝

-- ──────────────────────────────────────────────
-- TABLE 1: games (Game Engagement Data)
-- ──────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS games (
    game_id     INTEGER PRIMARY KEY,
    title       TEXT NOT NULL,
    release_date TEXT,
    release_year INTEGER,
    team        TEXT,                -- Developer studio
    rating      REAL,               -- User review score
    times_listed REAL,
    number_of_reviews REAL,
    genres      TEXT,               -- Comma-separated genres
    summary     TEXT,
    reviews     TEXT,
    plays       REAL,               -- Number of playthroughs
    playing     REAL,               -- Currently playing
    backlogs    REAL,               -- Users planning to play
    wishlist    REAL                 -- Users who wishlisted
);

-- ──────────────────────────────────────────────
-- TABLE 2: vgsales (Sales Data)
-- ──────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS vgsales (
    sale_id     INTEGER PRIMARY KEY,
    rank        INTEGER,
    name        TEXT NOT NULL,
    platform    TEXT,               -- Console/device
    year        INTEGER,            -- Release year
    genre       TEXT,               -- Main category
    publisher   TEXT,
    na_sales    REAL,               -- North America sales (millions)
    eu_sales    REAL,               -- Europe sales (millions)
    jp_sales    REAL,               -- Japan sales (millions)
    other_sales REAL,               -- Other regions (millions)
    global_sales REAL               -- Worldwide total (millions)
);

-- ──────────────────────────────────────────────
-- TABLE 3: merged_data (Combined Dataset)
-- ──────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS merged_data (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT,
    release_year INTEGER,
    team        TEXT,
    rating      REAL,
    genres      TEXT,
    plays       REAL,
    playing     REAL,
    backlogs    REAL,
    wishlist    REAL,
    platform    TEXT,
    year        INTEGER,
    genre       TEXT,
    publisher   TEXT,
    na_sales    REAL,
    eu_sales    REAL,
    jp_sales    REAL,
    other_sales REAL,
    global_sales REAL
);


-- ══════════════════════════════════════════════
-- SAMPLE QUERIES (Answering 30 EDA Questions)
-- ══════════════════════════════════════════════

-- Q1: Top-rated games by user reviews
SELECT title, rating, number_of_reviews, genres
FROM games
WHERE number_of_reviews > 100
ORDER BY rating DESC, number_of_reviews DESC
LIMIT 15;

-- Q2: Developers with highest average ratings (min 3 games)
SELECT team, 
       ROUND(AVG(rating), 2) AS avg_rating,
       COUNT(*) AS game_count
FROM games
WHERE team IS NOT NULL AND team != ''
GROUP BY team
HAVING game_count >= 3
ORDER BY avg_rating DESC
LIMIT 15;

-- Q3: Most common genres (requires app-level string splitting)
SELECT genres, COUNT(*) AS count
FROM games
WHERE genres IS NOT NULL
GROUP BY genres
ORDER BY count DESC
LIMIT 15;

-- Q4: Highest backlog-to-wishlist ratio
SELECT title, backlogs, wishlist,
       ROUND(CAST(backlogs AS FLOAT) / NULLIF(wishlist, 0), 2) AS ratio
FROM games
WHERE backlogs > 0 AND wishlist > 0
ORDER BY ratio DESC
LIMIT 15;

-- Q5: Game release trend by year
SELECT release_year AS year, COUNT(*) AS game_count
FROM games
WHERE release_year > 1980 AND release_year <= 2025
GROUP BY release_year
ORDER BY release_year;

-- Q7: Top 10 most wishlisted games
SELECT title, wishlist, rating, genres
FROM games
ORDER BY wishlist DESC
LIMIT 10;

-- Q9: Most productive developer studios
SELECT team, COUNT(*) AS games, ROUND(AVG(rating), 2) AS avg_rating,
       ROUND(SUM(plays), 0) AS total_plays
FROM games
WHERE team IS NOT NULL
GROUP BY team
HAVING games >= 3
ORDER BY total_plays DESC
LIMIT 15;

-- Q10: Sales by region
SELECT ROUND(SUM(na_sales), 2) AS north_america,
       ROUND(SUM(eu_sales), 2) AS europe,
       ROUND(SUM(jp_sales), 2) AS japan,
       ROUND(SUM(other_sales), 2) AS other
FROM vgsales;

-- Q11: Best-selling platforms
SELECT platform, ROUND(SUM(global_sales), 2) AS total_sales, COUNT(*) AS games
FROM vgsales
GROUP BY platform
ORDER BY total_sales DESC
LIMIT 15;

-- Q12: Releases and sales trend over years
SELECT year, COUNT(*) AS releases, ROUND(SUM(global_sales), 2) AS total_sales
FROM vgsales
WHERE year > 0
GROUP BY year
ORDER BY year;

-- Q13: Top publishers by sales
SELECT publisher, ROUND(SUM(global_sales), 2) AS total_sales, COUNT(*) AS games
FROM vgsales
WHERE publisher != 'Unknown'
GROUP BY publisher
ORDER BY total_sales DESC
LIMIT 15;

-- Q14: Top 10 global best-sellers
SELECT name, platform, year, genre, global_sales
FROM vgsales
ORDER BY global_sales DESC
LIMIT 10;

-- Q15: Regional sales by platform
SELECT platform,
       ROUND(SUM(na_sales), 2) AS na, ROUND(SUM(eu_sales), 2) AS eu,
       ROUND(SUM(jp_sales), 2) AS jp, ROUND(SUM(other_sales), 2) AS other
FROM vgsales
GROUP BY platform
ORDER BY SUM(global_sales) DESC
LIMIT 10;

-- Q17: Regional genre preferences
SELECT genre,
       ROUND(SUM(na_sales), 2) AS na, ROUND(SUM(eu_sales), 2) AS eu,
       ROUND(SUM(jp_sales), 2) AS jp, ROUND(SUM(other_sales), 2) AS other
FROM vgsales
GROUP BY genre
ORDER BY SUM(global_sales) DESC;

-- Q18: Yearly sales by region
SELECT year,
       ROUND(SUM(na_sales), 2) AS na, ROUND(SUM(eu_sales), 2) AS eu,
       ROUND(SUM(jp_sales), 2) AS jp, ROUND(SUM(other_sales), 2) AS other
FROM vgsales
WHERE year > 0
GROUP BY year
ORDER BY year;

-- Q19: Average sales per publisher
SELECT publisher, ROUND(AVG(global_sales), 2) AS avg_sales, COUNT(*) AS games
FROM vgsales
WHERE publisher != 'Unknown'
GROUP BY publisher
HAVING games >= 5
ORDER BY avg_sales DESC
LIMIT 15;

-- Q20: Top 5 games per platform (using window function)
SELECT platform, name, global_sales
FROM (
    SELECT platform, name, global_sales,
           ROW_NUMBER() OVER (PARTITION BY platform ORDER BY global_sales DESC) AS rn
    FROM vgsales
) sub
WHERE rn <= 5;

-- Q21: Genres by global sales (merged)
SELECT genre, ROUND(SUM(global_sales), 2) AS total_sales,
       ROUND(AVG(rating), 2) AS avg_rating, COUNT(*) AS games
FROM merged_data
GROUP BY genre
ORDER BY total_sales DESC;

-- Q22: Rating vs global sales
SELECT title, rating, global_sales
FROM merged_data
ORDER BY global_sales DESC;

-- Q23: Platforms with most highly-rated games (>4)
SELECT platform, COUNT(*) AS high_rated, ROUND(AVG(rating), 2) AS avg_rating
FROM merged_data
WHERE rating > 4
GROUP BY platform
ORDER BY high_rated DESC;

-- Q25: Wishlist vs sales correlation
SELECT title, wishlist, global_sales, rating
FROM merged_data
WHERE wishlist > 0 AND global_sales > 0
ORDER BY global_sales DESC;

-- Q29: Top genre + platform combinations
SELECT genre || ' + ' || platform AS combo,
       ROUND(SUM(global_sales), 2) AS total_sales, COUNT(*) AS games
FROM merged_data
GROUP BY genre, platform
HAVING games >= 2
ORDER BY total_sales DESC
LIMIT 15;

-- Q30: Regional heatmap by genre
SELECT genre,
       ROUND(SUM(na_sales), 2) AS na, ROUND(SUM(eu_sales), 2) AS eu,
       ROUND(SUM(jp_sales), 2) AS jp, ROUND(SUM(other_sales), 2) AS other
FROM merged_data
GROUP BY genre
ORDER BY SUM(global_sales) DESC;
