# kmeans_cluster.py - 改进版

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ✅ 路径请根据你的实际情况修改
file_path = "C:/Users/eirc/Desktop/9014/9014project/Valve_Player_Data.csv"
df = pd.read_csv(file_path)
df["Date"] = pd.to_datetime(df["Date"])

# 聚合特征：每个游戏的玩家行为特征
game_stats = df.groupby("Game_Name").agg({
    "Avg_players": ["mean", "std"],
    "Peak_Players": "mean"
}).dropna()

game_stats.columns = ["AvgPlayers_Mean", "AvgPlayers_Std", "PeakPlayers_Mean"]

# 标准化处理
scaler = StandardScaler()
scaled = scaler.fit_transform(game_stats)

# 聚类分析（k=3）
kmeans = KMeans(n_clusters=3, random_state=42)
game_stats["Cluster"] = kmeans.fit_predict(scaled)

# 可视化
plt.figure(figsize=(14, 8))

colors = ["tab:blue", "tab:orange", "tab:green"]
for cluster_id in sorted(game_stats["Cluster"].unique()):
    group = game_stats[game_stats["Cluster"] == cluster_id]
    plt.scatter(
        group["AvgPlayers_Mean"], 
        group["PeakPlayers_Mean"], 
        label=f"Cluster {cluster_id}",
        s=60,
        color=colors[cluster_id]
    )
    # 每个聚类显示一个游戏名字作为代表
    sample = group.sort_values("AvgPlayers_Mean", ascending=False).head(3)
    for name, row in sample.iterrows():
        plt.text(row["AvgPlayers_Mean"], row["PeakPlayers_Mean"], name, fontsize=8)

# 设置坐标轴为对数，以避免左下角过度挤压
# 设置坐标轴为对数，以避免左下角过度挤压
plt.xscale("log")
plt.yscale("log")

plt.xlabel("Average Players (log scale)")
plt.ylabel("Peak Players (log scale)")
plt.title("Steam Game Clustering (KMeans, log-log)")
plt.legend()
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.tight_layout()

# ✅ 保存图像
output_path = "C:/Users/eirc/Desktop/9014/9014project/charts/kmeans_cluster.png"
plt.savefig(output_path)
plt.close()
print(f"✅ Plot saved to: {output_path}")

