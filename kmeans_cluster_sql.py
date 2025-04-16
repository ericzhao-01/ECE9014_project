import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

# === 1. Connect to MySQL ===
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2018Happy!",
    database="steam_analysis"
)
query = """
    SELECT 
        g.name AS game_name,
        AVG(ms.avg_players) AS avg_players,
        AVG(ms.peak_players) AS peak_players
    FROM monthly_stats ms
    JOIN games g ON ms.game_id = g.game_id
    GROUP BY g.name
    HAVING avg_players IS NOT NULL AND peak_players IS NOT NULL
"""
df = pd.read_sql(query, conn)
conn.close()

# === 2. Feature preparation ===
df = df.dropna()
features = df[["avg_players", "peak_players"]]
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# === 3. Clustering ===
kmeans = KMeans(n_clusters=3, random_state=42)
df["cluster"] = kmeans.fit_predict(scaled_features)

# === 4. Visualization ===
plt.figure(figsize=(12, 8))
colors = ['tab:blue', 'tab:orange', 'tab:green']

for i in range(3):
    cluster = df[df["cluster"] == i]
    plt.scatter(
        cluster["avg_players"], cluster["peak_players"],
        s=60, label=f"Cluster {i}", color=colors[i]
    )
    # 标注代表游戏
    top = cluster.sort_values("avg_players", ascending=False).head(3)
    for _, row in top.iterrows():
        plt.text(row["avg_players"], row["peak_players"], row["game_name"], fontsize=8)

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Average Players (log scale)")
plt.ylabel("Peak Players (log scale)")
plt.title("Steam Game Clustering (SQL-based KMeans, log-log)")
plt.legend()
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.tight_layout()

# === 5. Save ===
chart_path = "charts/kmeans_cluster_sql.png"
plt.savefig(chart_path)
plt.close()
chart_path
