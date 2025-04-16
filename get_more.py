import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_game_details(game_name):
    try:
        search_url = f"https://steamcommunity.com/actions/SearchApps/{game_name}"
        resp = requests.get(search_url, headers=headers, timeout=10)
        app_list = resp.json()
        if not app_list:
            return "N/A", "N/A", "N/A"
        appid = app_list[0]["appid"]

        detail_url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        detail_resp = requests.get(detail_url, headers=headers, timeout=10)
        game_data = detail_resp.json()[str(appid)]["data"]

        genre = game_data["genres"][0]["description"] if "genres" in game_data else "N/A"
        developer = game_data["developers"][0] if "developers" in game_data else "N/A"
        release = game_data["release_date"]["date"]
        release_year = release.split()[-1] if release else "N/A"

        return genre, developer, release_year
    except:
        return "N/A", "N/A", "N/A"

def safe_int(text):
    text = text.strip().replace(",", "")
    return int(text) if text.isdigit() else 0

def scrape_steam_top100():
    all_data = []
    today = datetime.now().strftime("%Y-%m-%d")
    rank_counter = 1

    for page in range(1, 5):  # p.1 to p.4 = 100 games
        url = f"https://steamcharts.com/top/p.{page}"
        print(f"📥 Fetching {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", class_="common-table")
            rows = table.find_all("tr")[1:]

            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 5:
                    try:
                        name = cols[1].text.strip()
                        current = safe_int(cols[2].text)
                        peak = safe_int(cols[4].text)
                        ratio = round(current / peak, 3) if peak > 0 else 0

                        genre, dev, year = get_game_details(name)

                        all_data.append([
                            today, rank_counter, name, current, peak, ratio,
                            genre, dev, year
                        ])
                        print(f"#{rank_counter}: {name} ✅")
                        rank_counter += 1
                        time.sleep(1)
                    except Exception as e:
                        print(f"⚠️ Error parsing row: {e}")
        except Exception as e:
            print(f"❌ Failed to fetch {url}: {e}")

    return all_data

# Run and export
data = scrape_steam_top100()

df = pd.DataFrame(data, columns=[
    "Date", "Rank", "Game", "Current Players", "Peak Today",
    "Heat Ratio", "Genre", "Developer", "Release Year"
])

filename = f"Steam_Top100_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
df.to_excel(filename, index=False, engine="openpyxl")

print(f"\n✅ Exported to {filename} ({len(df)} rows)")
