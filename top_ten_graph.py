# top_ten_graph.py

import pandas as pd
import matplotlib.pyplot as plt
import os

# ✅ 你的 CSV 路径
file_path = "C:/Users/eirc/Desktop/9014/9014project/Valve_Player_Data.csv"

# ✅ 输出图片路径
output_path = "C:/Users/eirc/Desktop/9014/9014project/charts/top_ten_graph.png"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# === 读取数据 ===
df = pd.read_csv(file_path)
df["Date"] = pd.to_datetime(df["Date"])

# === 找到 Top 10 游戏 ===
top10_games = (
    df.groupby("Game_Name")["Avg_players"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .index.tolist()
)

df_top10 = df[df["Game_Name"].isin(top10_games)]

# === 生成趋势矩阵 ===
pivot_df = df_top10.pivot_table(index="Date", columns="Game_Name", values="Avg_players")

# === 绘图 ===
plt.figure(figsize=(14, 8))
for game in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[game], label=game)

plt.title("Top 10 Steam Games - Average Players Over Time")
plt.xlabel("Date")
plt.ylabel("Average Players")
plt.legend(loc="upper left")
plt.grid(True)
plt.tight_layout()

# ✅ 保存图像
plt.savefig(output_path)
plt.close()
print(f"✅ Saved to: {output_path}")
