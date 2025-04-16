import streamlit as st
from PIL import Image
import os

# ==== Config ====
st.set_page_config(page_title="Steam Game Analysis Dashboard", layout="wide")
chart_dir = "charts"
seasonality_dir = "seasonality_plots"

# ==== Title ====
st.title("🎮 Steam Game Analysis Dashboard")

# ==== Sidebar: Interactive Controls ====
st.sidebar.header("🔧 Controls")
selected_seasonal_game = st.sidebar.selectbox(
    "Select a game for seasonal decomposition:",
    ["counter_strike_global_offensive", "dota_2", "rust", "warframe", "grand_theft_auto_v"],
    format_func=lambda x: x.replace("_", " ").title()
)

# ==== Tabs ====
tabs = st.tabs(["Top 10 Trends", "Forecasting", "Seasonality", "Event Impact", "Clustering"])

# --- Tab 1: Top Games ---
with tabs[0]:
    st.header("📈 Top 10 Player Trends")
    img_path = os.path.join(chart_dir, "top_ten_graph.png")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.error(f"❌ File not found: {img_path}")

# --- Tab 2: Forecasting ---
with tabs[1]:
    st.header("🔮 Forecasting (ARIMA)")
    img_path = os.path.join(chart_dir, "multi_game_forecast.png")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.error(f"❌ File not found: {img_path}")

# --- Tab 3: Seasonality ---
with tabs[2]:
    st.header("📅 Seasonal Decomposition")
    img_path = os.path.join(seasonality_dir, f"{selected_seasonal_game}_seasonality.png")
    st.subheader(selected_seasonal_game.replace("_", " ").title())
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.error(f"❌ File not found: {img_path}")

# --- Tab 4: Event Impact ---
with tabs[3]:
    st.header("📌 Top 5 Games – Event-Annotated Trends")
    img_path = os.path.join(chart_dir, "top5_games_event_annotated.png")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.error(f"❌ File not found: {img_path}")

# --- Tab 5: Clustering ---
with tabs[4]:
    st.header("🧩 Game Clustering (KMeans)")
    img_path = os.path.join(chart_dir, "kmeans_cluster.png")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.error(f"❌ File not found: {img_path}")
