# top5_event_annotation_plot.py
# Plot average player trends for 5 similar-scale games with major event annotations

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# === 1. Load and prepare data ===
file_path = "C:/Users/eirc/Desktop/9014/9014project/Valve_Player_Data.csv"
df = pd.read_csv(file_path)
df["Date"] = pd.to_datetime(df["Date"])

# === 2. Create pivot table (Date x Game) ===
pivot_df = df.pivot_table(index="Date", columns="Game_Name", values="Avg_players")
pivot_df = pivot_df.asfreq("MS").interpolate(method="linear")

# === 3. Filter games with long history (≥ 5 years) and smooth scale ===
min_year = 2014
min_points = 60  # Minimum 5 years of monthly data

# Step 1: history filter
valid_games = []
for game in pivot_df.columns:
    series = pivot_df[game].dropna()
    if series.index.min().year <= min_year and len(series) >= min_points:
        valid_games.append(game)

# Step 2: filter by overall average player count (20k–400k)
overall_avg = pivot_df.mean().dropna()
filtered_games = [g for g in valid_games if 20000 < overall_avg.get(g, 0) < 400000]

# Step 3: select top 5 by overall average
selected_games = sorted(filtered_games, key=lambda g: overall_avg[g], reverse=True)[:5]

# === 4. Plot trends with event annotations ===
plt.figure(figsize=(15, 8))
colors = ['steelblue', 'darkorange', 'green', 'crimson', 'purple']

for i, game in enumerate(selected_games):
    series = pivot_df[game].dropna()
    plt.plot(series.index, series.values, label=game, linewidth=2, color=colors[i])

# === 5. Key events to annotate ===
events = {
    "2015-06": "TF2 Gun Mettle",
    "2018-12": "CSGO Free",
    "2020-03": "COVID-19",
    "2020-06": "Rust Twitch Boost",
    "2023-03": "Steam Deck"
}

for date_str, label in events.items():
    date = pd.to_datetime(date_str)
    plt.axvline(x=date, color='gray', linestyle='--', alpha=0.5)
    plt.text(date, plt.ylim()[1]*0.95, label, rotation=90, color='gray', fontsize=9, ha='right')

# === 6. Layout & save ===
plt.title("Top 5 Games – Player Trends with Key Events", fontsize=16)
plt.xlabel("Date")
plt.ylabel("Average Players")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.3)
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.xticks(rotation=45)
plt.tight_layout()

# Save figure
output_path = "C:/Users/eirc/Desktop/9014/9014project/charts/top5_games_event_annotated.png"
plt.savefig(output_path)
plt.close()
print(f"✅ Plot saved to: {output_path}")

