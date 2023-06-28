from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from datetime import datetime
from datetime import date
import sqlite3

conn = sqlite3.connect("Database/app_store_stats.db")
cursor = conn.cursor()


def fetch_data(urliOS):
    result = requests.get(urliOS)
    soup = BeautifulSoup(result.content, "lxml")
    rank_element = soup.find("a", {"class": "inline-list__item"})
    rank = None
    if rank_element is not None:
        rank_text = rank_element.text.strip()
        rank_text = rank_text.split()[0]
        rank = int(rank_text.replace(",", "").replace("#", ""))
    script = soup.find(type="application/ld+json").text.strip()
    data = json.loads(script)

    app_rating = None
    review_count = None
    if "aggregateRating" in data:
        app_rating = data["aggregateRating"].get("ratingValue")
        review_count = data["aggregateRating"].get("reviewCount")

    dataApp = {
        "App Name": data.get("name"),
        "iOS App Rating": app_rating,
        "iOS Total Reviews": review_count,
        "iOS Rank": rank,
    }
    return dataApp


dataiOS = []
for link in urliOS:
    dataApp = fetch_data(link)
    dataiOS.append(dataApp)

dataiOS = pd.DataFrame(
    dataiOS,
    index=[
        "GKW",
        "MAF",
        "SAEM",
        "CA",
        "MV",
        "MC",
        "MD",
        "TM",
        "XM",
        "SNLS",
        "MSA",
        "MSP",
        "VMF",
        "MCL",
        "VM",
        "SU",
        "STVA",
        "ATT",
        "SSLG",
        "MDCM",
        "MM",
        "MFR",
        "XF",
        "GFBR",
        "MVIA",
        "ARM",
        "ASTRCN",
        "HUGH",
        "HTMYA",
        "MIDCO",
        "OPTS",
        "USCELL",
        "SEC",
        "OPTTV",
        "BRE",
        "BLUER",
        "BUCK",
    ],
)
now = datetime.now()
dataiOS.insert(0, "Date", now.strftime("%B %d, %Y"))
dataiOS.insert(0, "Detail Date", now.strftime("%Y-%m-%d %H:%M:%S"))
dataiOS.to_excel("iOSratings.xlsx")

today = date.today().strftime("%Y-%m-%d")
unique_dataiOS = dataiOS[dataiOS["Detail Date"].str.startswith(today)].copy()

cursor.execute(f"SELECT * FROM dataiOS WHERE [Date] = '{now.strftime('%B %d, %Y')}'")
existing_data = cursor.fetchall()

if existing_data:
    cursor.execute(f"DELETE FROM dataiOS WHERE [Date] = '{now.strftime('%B %d, %Y')}'")
    conn.commit()

unique_dataiOS.to_sql("dataiOS", conn, if_exists="append", index=True)

conn.commit()
conn.close()
