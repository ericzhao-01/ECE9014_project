import requests
from bs4 import BeautifulSoup
import pandas as pd

# Simulate a browser request header to avoid being blocked by the website
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Define the target URL to scrape data from
url = "https://steamcharts.com/top"

# Send an HTTP GET request to fetch the webpage content
response = requests.get(url, headers=headers)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Locate the table containing the game ranking and player statistics
table = soup.find("table", class_="common-table")
rows = table.find_all("tr")[1:]  # Skip the header row

# Initialize an empty list to store the extracted data
data = []

# Define a helper function to safely convert strings to integers
def safe_int(text):
    text = text.strip().replace(",", "")
    return int(text) if text.isdigit() else 0

# Loop through each row in the table and extract relevant columns
for row in rows:
    cols = row.find_all("td")
    if len(cols) >= 5:
        try:
            # Extract and clean each field
            rank = int(cols[0].text.strip().replace(".", ""))
            name = cols[1].text.strip()
            current_players = safe_int(cols[2].text)
            peak_today = safe_int(cols[4].text)
            
            # Calculate heat ratio (current players / today's peak)
            heat_ratio = round(current_players / peak_today, 3) if peak_today > 0 else 0

            # Append the cleaned row to the dataset
            data.append([rank, name, current_players, peak_today, heat_ratio])
        except:
            # Skip any rows with malformed data
            continue

# Create a pandas DataFrame from the collected data
df = pd.DataFrame(data, columns=["Rank", "Game", "Current Players", "Peak Today", "Heat Ratio"])

# Export the cleaned data to a CSV file
df.to_csv("Steam_Top100.csv", index=False)
print("✅ Saved as Steam_Top100.csv")
