import pandas as pd
import mysql.connector

# 读取 CSV 文件
file_path = "C:/Users/eirc/Desktop/9014/9014project/Valve_Player_Data.csv"
df = pd.read_csv(file_path)
df["Date"] = pd.to_datetime(df["Date"])

# 连接 MySQL 数据库
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2018Happy!",
    database="steam_analysis"
)
cursor = conn.cursor()

# 插入游戏名称（去重）
game_name_to_id = {}
unique_games = df["Game_Name"].unique()

for game in unique_games:
    cursor.execute("INSERT IGNORE INTO games (name) VALUES (%s)", (game,))
conn.commit()

# 生成游戏名到 ID 的映射
cursor.execute("SELECT game_id, name FROM games")
for gid, name in cursor.fetchall():
    game_name_to_id[name] = gid

# 插入玩家数据
for _, row in df.iterrows():
    game_id = game_name_to_id.get(row["Game_Name"])
    if game_id:
        cursor.execute(
            """
            INSERT INTO monthly_stats (game_id, date, avg_players, peak_players)
            VALUES (%s, %s, %s, %s)
            """,
            (game_id, row["Date"].date(), int(row["Avg_players"]), int(row["Peak_Players"]))
        )

conn.commit()
cursor.close()
conn.close()

print("✅ Data imported successfully.")
