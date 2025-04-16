import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import os

# 读取数据
file_path = "C:/Users/eirc/Desktop/9014/9014project/Valve_Player_Data.csv"
df = pd.read_csv(file_path)
df["Date"] = pd.to_datetime(df["Date"])

# 指定预测的中等体量游戏（也可以自选）
games = ['Apex Legends', 'Rust', 'Destiny 2', 'Warframe', 'Team Fortress 2']
forecast_horizon = 3  # 预测未来几个月

# 输出路径
output_path = "C:/Users/eirc/Desktop/9014/9014project/charts/multi_game_forecast.png"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

plt.figure(figsize=(14, 7))

# 保存预测起始时间，用于绘制预测区域
latest_date = df["Date"].max()
future_index = pd.date_range(start=latest_date + pd.DateOffset(months=1), periods=forecast_horizon, freq='MS')

for game in games:
    game_df = df[df["Game_Name"] == game].sort_values("Date")
    ts = game_df.set_index("Date")["Avg_players"]
    
    # 拟合 ARIMA 模型并预测
    model = ARIMA(ts, order=(1, 1, 1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecast_horizon)
    
    forecast_series = pd.Series(forecast.values, index=future_index)
    full_series = pd.concat([ts, forecast_series])

    # 绘制历史和预测部分
    plt.plot(full_series.index, full_series.values, label=game, linewidth=2)

# 灰色背景表示预测区域
plt.axvspan(future_index[0], future_index[-1], color='lightgray', alpha=0.3, label='Forecast Range')

# 美化图表
plt.title("📈 Multi-Game Average Player Forecast (ARIMA)", fontsize=16)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Average Players", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(title="Game", fontsize=10)
plt.tight_layout()

# ✅ 保存图像
plt.savefig(output_path)
print(f"✅ Forecast figure saved to: {output_path}")

plt.close()
