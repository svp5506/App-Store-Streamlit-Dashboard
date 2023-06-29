from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import sqlite3

conn = sqlite3.connect("Database/app_store_stats.db")
cursor = conn.cursor()


def process_url(link):
    resultAndroid = requests.get(link)
    soupAndroid = BeautifulSoup(resultAndroid.content, "lxml")
    starRatingRaw = soupAndroid.find("div", {"class": "TT9eCd"})

    if starRatingRaw is not None:
        starRating = starRatingRaw.text.replace("star", "")
    else:
        starRating = ""

    appName = soupAndroid.find("h1", {"itemprop": "name"})
    appName = appName.text

    temp_list = [None] * 8
    temp_list[0] = datetime.now().strftime("%B %d, %Y")  # Date
    temp_list[6] = starRating  # Star Rating
    temp_list[7] = appName  # App Name

    divReviews = soupAndroid.find_all("div", {"class": "RutFAf wcB8se"})
    if divReviews:
        for i, div in enumerate(divReviews):
            countReviewsRaw = div["title"]
            countReviews = countReviewsRaw.replace(",", "")
            temp_list[i + 1] = int(countReviews)
    return temp_list


dataAndroid = []
for link in urlAndroid:
    temp_list = process_url(link)
    dataAndroid.append(temp_list)

dataAndroid = pd.DataFrame(
    dataAndroid,
    columns=[
        "Date",
        "5 Star Reviews",
        "4 Star Reviews",
        "3 Star Reviews",
        "2 Star Reviews",
        "1 Star Reviews",
        "Android App Rating",
        "App Name",
    ],
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

dataAndroid["Android Total Reviews"] = dataAndroid.loc[
    :, "5 Star Reviews":"1 Star Reviews"
].sum(1)
dataAndroid = dataAndroid[
    [
        "Date",
        "App Name",
        "Android App Rating",
        "Android Total Reviews",
        "5 Star Reviews",
        "4 Star Reviews",
        "3 Star Reviews",
        "2 Star Reviews",
        "1 Star Reviews",
    ]
]

dataAndroid.to_sql("dataAndroid", conn, if_exists="replace", index=True)
conn.commit()
conn.close()
