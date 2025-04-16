# seasonality_batch.py
# Final version: manually plot all 4 components with correct X-axis formatting

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.seasonal import seasonal_decompose
import os

# ✅ Path to CSV data file
file_path = "C:/Users/eirc/Desktop/9014/9014project/Valve_Player_Data.csv"
df = pd.read_csv(file_path)
df["Date"] = pd.to_datetime(df["Date"])

# ✅ List of selected games with sufficient history
games = [
    "Counter Strike: Global Offensive",
    "Dota 2",
    "Rust",
    "Grand Theft Auto V",
    "Warframe"
]

# ✅ Output folder for seasonal plots
output_dir = "C:/Users/eirc/Desktop/9014/9014project/seasonality_plots"
os.makedirs(output_dir, exist_ok=True)

# ✅ Process each game
for game_name in games:
    game_df = df[df["Game_Name"] == game_name].sort_values("Date")
    ts = game_df.set_index("Date")["Avg_players"]
    ts = ts.asfreq("MS").interpolate(method="linear")

    if len(ts) < 24:
        print(f"⚠️ Skipped: {game_name} has less than 24 months of data.")
        continue

    try:
        result = seasonal_decompose(ts, model='additive', period=12)

        # ✅ Manually create subplot for each component
        fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=False)
        components = ['observed', 'trend', 'seasonal', 'resid']
        titles = ['Observed', 'Trend', 'Seasonal', 'Residual']

        for i, comp in enumerate(components):
            ax = axes[i]
            data = getattr(result, comp)

            if comp == "seasonal":
                # ✅ Aggregate seasonality across all years to form 1 typical year cycle
                monthly_avg = data.groupby(data.index.month).mean()
                ax.plot(range(1, 13), monthly_avg.values, marker='o')
                ax.set_xticks(range(1, 13))
                ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
                ax.set_xlabel("Month (1–12)")
            else:
                ax.plot(data)
                ax.set_xlabel("Date")
                ax.xaxis.set_major_locator(mdates.YearLocator(2))
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
                ax.tick_params(axis='x', labelrotation=45)

            ax.set_ylabel(titles[i], fontsize=12)

        fig.suptitle(f"Seasonal Decomposition of {game_name}", fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])

        # ✅ Save final figure
        safe_name = game_name.replace(" ", "_").replace(":", "").lower()
        output_path = os.path.join(output_dir, f"{safe_name}_seasonality.png")
        plt.savefig(output_path)
        plt.close()

        print(f"✅ Saved: {game_name} → {output_path}")

    except Exception as e:
        print(f"❌ Error processing {game_name}: {e}")
