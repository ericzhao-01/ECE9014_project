# top5_sql_plot.py

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# === 数据库连接 ===
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2018Happy!",  # ⚠️改成你的密码
    database="steam_analysis"
)

# 前 5 名游戏（来自 SQL 查询）
top5_games = [
    "Dota 2",
    "PUBG: Battlegrounds",
    "Counter Strike: Global Offensive",
    "Apex Legends",
    "Valheim"
]

all_data = []

# === 逐个查询每个游戏的时间序列 ===
for game in top5_games:
    query = """
        SELECT ms.date, ms.avg_players
        FROM monthly_stats ms
        JOIN games g ON ms.game_id = g.game_id
        WHERE g.name = %s
        ORDER BY ms.date;
    """
    df = pd.read_sql(query, conn, params=(game,))
    df["Game"] = game
    all_data.append(df)

conn.close()

# 合并成一个 DataFrame
df_all = pd.concat(all_data)

# === 可视化 ===
plt.figure(figsize=(16, 8))
for game in top5_games:
    df_game = df_all[df_all["Game"] == game]
    plt.plot(df_game["date"], df_game["avg_players"], label=game)

plt.title("🎮 Top 5 Steam Games – Avg Players Over Time", fontsize=18)
plt.xlabel("Date")
plt.ylabel("Average Players")
plt.grid(True, linestyle="--", alpha=0.4)
plt.legend(title="Game", fontsize=10)
plt.xticks(rotation=45)
plt.tight_layout()

# 保存图片
plt.savefig("charts/top5_avg_players_sql.png")
plt.show()
