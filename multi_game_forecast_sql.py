import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.arima.model import ARIMA
import os

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2018Happy!",
    database="steam_analysis"
)

games = ["Destiny 2", "Grand Theft Auto V", "NARAKA: BLADEPOINT", "Team Fortress 2", "Tom Clancy's Rainbow Six Seige"]
forecast_horizon = 3

plt.figure(figsize=(14, 7))

for game in games:
    query = f"""
        SELECT ms.date, ms.avg_players
        FROM monthly_stats ms
        JOIN games g ON ms.game_id = g.game_id
        WHERE g.name = %s
        ORDER BY ms.date
    """
    df = pd.read_sql(query, conn, params=(game,))
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    ts = df['avg_players'].asfreq('MS').interpolate()

    if len(ts) < 24:
        continue

    model = ARIMA(ts, order=(1, 1, 1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecast_horizon)

    forecast_index = pd.date_range(start=ts.index[-1] + pd.DateOffset(months=1), periods=forecast_horizon, freq='MS')
    forecast_series = pd.Series(forecast.values, index=forecast_index)

    full_series = pd.concat([ts, forecast_series])
    plt.plot(full_series.index, full_series.values, label=game)

plt.axvspan(forecast_index[0], forecast_index[-1], color='lightgray', alpha=0.3, label='Forecast Range')
plt.title("📈 Rank 6-10 Games – ARIMA Forecast", fontsize=16)
plt.xlabel("Date")
plt.ylabel("Average Players")
plt.legend(title="Game", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.5)
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.xticks(rotation=45)
plt.tight_layout()

output_path = "charts/top10_6to10_forecast_sql.png"
plt.savefig(output_path)
plt.close()
print(f"✅ Saved to: {output_path}")
