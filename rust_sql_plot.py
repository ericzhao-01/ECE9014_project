# rust_sql_plot.py

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# === 1. 连接数据库 ===
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2018Happy!",  # ← 替换成你刚设好的密码
    database="steam_analysis"
)

query = """
    SELECT ms.date, ms.avg_players
    FROM monthly_stats ms
    JOIN games g ON ms.game_id = g.game_id
    WHERE g.name = 'Rust'
    ORDER BY ms.date;
"""

# === 2. 读取数据 ===
df = pd.read_sql(query, conn)
conn.close()

# === 3. 画图 ===
plt.figure(figsize=(14, 6))
plt.plot(df["date"], df["avg_players"], marker='o', linestyle='-', color='orange', label='Rust')
plt.title("📈 Rust - Avg Players Over Time", fontsize=16)
plt.xlabel("Date")
plt.ylabel("Average Players")
plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()

# === 4. 可选：保存图片 ===
plt.savefig("charts/rust_avg_players_sql.png")
plt.show()
