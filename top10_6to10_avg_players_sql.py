import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import os

# === 连接数据库 ===
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2018Happy!",  # ← 你的 MySQL 密码
    database="steam_analysis"
)

query = """
SELECT g.name, ms.date, ms.avg_players
FROM monthly_stats ms
JOIN games g ON ms.game_id = g.game_id
WHERE g.name IN (
    'Destiny 2',
    'Grand Theft Auto V',
    'Team Fortress 2',
    'Tom Clancy''s Rainbow Six Seige'
)
ORDER BY g.name, ms.date;
"""

df = pd.read_sql(query, conn)
conn.close()

# === 绘图 ===
plt.figure(figsize=(15, 8))
for game, group in df.groupby("name"):
    plt.plot(group["date"], group["avg_players"], label=game)

plt.title("🎮 Rank 6-10 Steam Games – Avg Players Over Time")
plt.xlabel("Date")
plt.ylabel("Average Players")
plt.legend(title="Game")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

# === 保存图像 ===
output_path = "charts/top10_6to10_avg_players_sql.png"
os.makedirs("charts", exist_ok=True)
plt.savefig(output_path)
plt.close()
print(f"✅ Saved: {output_path}")
