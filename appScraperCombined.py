from bs4 import BeautifulSoup
import requests
import json
from datetime import date, datetime
import pandas as pd
import sqlite3
from urls import urlIOS, urlAndroid
from appKey import keyIOS, keyAndroid

# Access Database
conn = sqlite3.connect("Database/app_store_stats.db")
cursor = conn.cursor()


# Scrape iOS App Store Data
def scrapeDataIOS(urlIOS):
    result = requests.get(urlIOS)
    parse = BeautifulSoup(result.content, "lxml")
    script = parse.find(type="application/ld+json").text.strip()
    data = json.loads(script)

    # Retrieve and format App rank if available
    rank_element = parse.find("a", {"class": "inline-list__item"})
    rank = None
    if rank_element is not None:
        rank_text = rank_element.text.strip().split()[0]
        rank = int(rank_text.replace(",", "").replace("#", ""))

    # Retrieve App Rating and Review Count
    app_rating = None
    review_count = None
    if "aggregateRating" in data:
        app_rating = data["aggregateRating"].get("ratingValue")
        review_count = data["aggregateRating"].get("reviewCount")

    # Create columns for each field
    dataApp = {
        "App Name": data.get("name"),
        "iOS App Rating": app_rating,
        "iOS Total Reviews": review_count,
        "iOS Rank": rank,
    }
    return dataApp


# Append each new URL data with existing data
dataIOS = []
for link in urlIOS:
    dataApp = scrapeDataIOS(link)
    dataIOS.append(dataApp)

# Convert to dataframe and merge with keyIOS (unique ID for each app)
dataIOS = pd.DataFrame(dataIOS)
dataIOS = pd.merge(dataIOS, keyIOS, on="App Name", how="outer")
dataIOS.set_index("Mapping", inplace=True)

# Add timestamps
now = datetime.now()
dataIOS.insert(0, "Timestamp", now.strftime("%Y-%m-%d %H:%M:%S"))
dataIOS.insert(0, "Date", now.strftime("%B %d, %Y"))

# Check for duplicate data, App Data should exist for only one instance per day
today = date.today().strftime("%Y-%m-%d")
unique_dataIOS = dataIOS[dataIOS["Timestamp"].str.startswith(today)].copy()
cursor.execute(f"SELECT * FROM tableIOS WHERE [Date] = '{now.strftime('%B %d, %Y')}'")
existing_data = cursor.fetchall()
if existing_data:
    cursor.execute(f"DELETE FROM tableIOS WHERE [Date] = '{now.strftime('%B %d, %Y')}'")
    conn.commit()

# Add data to dataiOS Table if unique
unique_dataIOS.to_sql("tableIOS", conn, if_exists="append", index=True)
conn.commit()
conn.close()
