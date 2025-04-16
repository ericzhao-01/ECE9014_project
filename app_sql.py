import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import os
from PIL import Image

# ==== Config ====
st.set_page_config(page_title="Steam Game Analysis Dashboard (SQL)", layout="wide")
chart_dir = "charts"
seasonality_dir = "charts/seasonality_plots"

# ==== Helper to load image safely ====
def show_image(title, path):
    st.subheader(title)
    if os.path.exists(path):
        st.image(path, use_container_width=True)
    else:
        st.error(f"❌ File not found: {path}")

# ==== SQL helper ====
def run_sql_query(query):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2018Happy!",
            database="steam_analysis"
        )
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ SQL Error: {e}")
        return None

# ==== Sidebar Navigation ====
st.sidebar.title("🔵 Dashboard Navigation")
section = st.sidebar.radio("Select a Section:", [
    "Top Charts (SQL)",
    "Forecasting (SQL)",
    "Event Annotation (SQL)",
    "Clustering (SQL)",
    "Seasonality (Static)",
    "SQL Query Interface"
])

# ==== Top Charts ====
if section == "Top Charts (SQL)":
    st.title("📊 Top 10 Game Charts (SQL-Based)")
    show_image("Top 5 Games by Avg Players", os.path.join(chart_dir, "top5_avg_players_sql.png"))
    show_image("Rank 6-10 Games by Avg Players", os.path.join(chart_dir, "top10_6to10_avg_players_sql.png"))

# ==== Forecasting ====
elif section == "Forecasting (SQL)":
    st.title("🔮 Forecasting via ARIMA (SQL-Based)")
    show_image("Top 5 Games Forecast", os.path.join(chart_dir, "multi_game_forecast.png"))
    show_image("6-10 Games Forecast", os.path.join(chart_dir, "top10_6to10_forecast_sql.png"))

# ==== Event Annotation ====
elif section == "Event Annotation (SQL)":
    st.title("📌 Event-Annotated Player Trends")
    show_image("Top 5 Games with Event Tags", os.path.join(chart_dir, "top5_games_event_annotated_sql.png"))

# ==== Clustering ====
elif section == "Clustering (SQL)":
    st.title("🧹 Steam Game Clustering (SQL)")
    show_image("KMeans Cluster Visualization", os.path.join(chart_dir, "kmeans_cluster_sql.png"))

# ==== Seasonality (Static) ====
elif section == "Seasonality (Static)":
    st.title("🗕️ Seasonal Decomposition (Static CSV-Based)")
    game = st.selectbox("Choose a Game: ", [
        "counter_strike_global_offensive",
        "dota_2",
        "grand_theft_auto_v",
        "rust",
        "warframe"
    ])
    safe_name = f"{game}_seasonality.png"
    show_image(game.replace("_", " ").title(), os.path.join(seasonality_dir, safe_name))

# ==== SQL Query Interface ====
elif section == "SQL Query Interface":
    st.title("🧠 Run Custom SQL Queries")
    st.markdown("_Choose a query preset or write your own below._")

    # --- Presets ---
    preset_options = {
        "Top 10 Games by Avg Players":
            "SELECT name, AVG(avg_players) AS avg_player_count FROM monthly_stats JOIN games ON games.game_id = monthly_stats.game_id GROUP BY name ORDER BY avg_player_count DESC LIMIT 10;",

        "Rust Avg Players Since 2015":
            "SELECT ms.date, ms.avg_players FROM monthly_stats ms JOIN games g ON ms.game_id = g.game_id WHERE g.name = 'Rust' AND ms.date >= '2015-01-01' ORDER BY ms.date;",

        "Top Yearly Growth Games":
            "SELECT g.name, YEAR(ms.date) AS year, MAX(ms.avg_players) - MIN(ms.avg_players) AS yearly_growth FROM monthly_stats ms JOIN games g ON ms.game_id = g.game_id GROUP BY g.name, YEAR(ms.date) HAVING COUNT(*) >= 6 ORDER BY yearly_growth DESC LIMIT 10;",

        "Top Games with Over 1M Peak Players":
            "SELECT g.name, MAX(ms.peak_players) AS peak FROM monthly_stats ms JOIN games g ON ms.game_id = g.game_id GROUP BY g.name HAVING peak > 1000000 ORDER BY peak DESC;",

    }

    selected_preset = st.selectbox("📚 Choose a preset:", list(preset_options.keys()))
    query_input = st.text_area("📝 Edit or write your SQL below:", value=preset_options[selected_preset], height=180)

    # --- Run Query ---
    if st.button("Run Query"):
        df = run_sql_query(query_input)
        if df is not None:
            if not df.empty:
                st.success(f"✅ Query executed successfully. {len(df)} rows returned.")
                st.dataframe(df)

                # Optional Plot
                if "date" in df.columns and df.select_dtypes("number").shape[1] == 1:
                    st.line_chart(data=df.set_index("date"))
                elif df.shape[1] == 2 and df.dtypes[1] in ['int64', 'float64']:
                    st.bar_chart(data=df.set_index(df.columns[0]))
            else:
                st.warning("⚠️ Query returned no results.")
