import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.seasonal import seasonal_decompose
import os

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2018Happy!",
    database="steam_analysis"
)

# ✅ Selected games
games = [
    "Counter Strike: Global Offensive",
    "Dota 2",
    "Rust",
    "Grand Theft Auto V",
    "Warframe"
]

# ✅ Output directory
output_dir = "charts/seasonality_plots"
os.makedirs(output_dir, exist_ok=True)

# ✅ Generate seasonality decomposition plots
for game_name in games:
    query = f"""
    SELECT ms.date, ms.avg_players
    FROM monthly_stats ms
    JOIN games g ON ms.game_id = g.game_id
    WHERE g.name = '{game_name}'
    ORDER BY ms.date;
    """
    df = pd.read_sql(query, conn)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    ts = df["avg_players"].asfreq("MS").interpolate(method="linear")

    if len(ts) < 24:
        print(f"⚠️ Skipped: {game_name} has less than 24 months of data.")
        continue

    try:
        result = seasonal_decompose(ts, model="additive", period=12)
        fig, axes = plt.subplots(4, 1, figsize=(12, 10))
        components = ["observed", "trend", "seasonal", "resid"]
        titles = ["Observed", "Trend", "Seasonal", "Residual"]

        for i, comp in enumerate(components):
            ax = axes[i]
            data = getattr(result, comp)
            if comp == "seasonal":
                monthly_avg = data.groupby(data.index.month).mean()
                ax.plot(range(1, 13), monthly_avg.values, marker="o")
                ax.set_xticks(range(1, 13))
                ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
                ax.set_xlabel("Month (1–12)")
            else:
                ax.plot(data)
                ax.set_xlabel("Date")
                ax.xaxis.set_major_locator(mdates.YearLocator(2))
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
                ax.tick_params(axis="x", labelrotation=45)

            ax.set_ylabel(titles[i], fontsize=12)

        fig.suptitle(f"Seasonal Decomposition of {game_name}", fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        safe_name = game_name.replace(" ", "_").replace(":", "").lower()
        output_path = os.path.join(output_dir, f"{safe_name}_seasonality.png")
        plt.savefig(output_path)
        plt.close()
        print(f"✅ Saved: {game_name} → {output_path}")
    except Exception as e:
        print(f"❌ Error processing {game_name}: {e}")

conn.close()
