import pandas as pd
from datetime import datetime
import sqlite3

# Read data from files with specified data types
dataiOS = pd.read_excel("iOSratings.xlsx")
dataAndroid = pd.read_excel("androidRatings.xlsx")

# Sort Android ratings by App Name
# dataAndroid.sort_values('App Name', inplace=True)

# Merge iOS and Android Dataframes
dataCombined = dataiOS.join(dataAndroid, how="outer", rsuffix="_Android")

# Drop unnecessary columns
dataCombined.drop(
    columns=[
        "App Name_Android",
        "Date_Android",
        "5 Star Reviews",
        "4 Star Reviews",
        "3 Star Reviews",
        "2 Star Reviews",
        "1 Star Reviews",
        "Detail Date",
    ],
    inplace=True,
)
dataCombined.reset_index(drop=True)

# Convert columns to numeric types
dataCombined["iOS App Rating"] = pd.to_numeric(
    dataCombined["iOS App Rating"], errors="coerce"
)
dataCombined["Android App Rating"] = pd.to_numeric(
    dataCombined["Android App Rating"], errors="coerce"
)
dataCombined["iOS Total Reviews"] = pd.to_numeric(
    dataCombined["iOS Total Reviews"], errors="coerce"
)
dataCombined["Android Total Reviews"] = pd.to_numeric(
    dataCombined["Android Total Reviews"], errors="coerce"
)
dataCombined["iOS Rank"] = pd.to_numeric(dataCombined["iOS Rank"], errors="coerce")

# Calculate average App Rating
dataCombined["Overall App Rating"] = (
    dataCombined["iOS App Rating"] + dataCombined["Android App Rating"]
) / 2

# Calculate total reviews
dataCombined["Total Reviews"] = dataCombined["iOS Total Reviews"].add(
    dataCombined["Android Total Reviews"], fill_value=0
)

# Simplify Date Format
dataCombined["Date"] = pd.to_datetime(dataCombined["Date"]).dt.strftime("%B %d, %Y")

# Reorder columns
dataCombined = dataCombined[
    [
        "Date",
        "App Name",
        "Overall App Rating",
        "Total Reviews",
        "iOS App Rating",
        "iOS Total Reviews",
        "iOS Rank",
        "Android App Rating",
        "Android Total Reviews",
    ]
]
