import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import streamlit as st
from PIL import Image


st.set_page_config(page_title="App Ratings", layout="wide")

#! CSS Style Sheet
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Heading Section [MSA Logo, Page Title]
logoMSA = Image.open("images/logoMSA.png")

#! CONTAINER ONE
with st.container():
    col1, col2 = st.columns([1, 10])
    with col1:
        st.image(logoMSA, output_format="PNG", width=100)
    with col2:
        st.title(":blue[My Spectrum App] Insights")


# Retrieve App Stats from tableCombined
def get_app_stats(
    excludeApps=[], app_name="", timestamp="", conn=None, minTotalReviews=150000
):
    c = conn.cursor()
    c.execute(
        """
        SELECT `App Name`, `Avg App Rating`, `Total Reviews`, `Date`, App_Ranking
        FROM (
            SELECT `App Name`, `Avg App Rating`, `Total Reviews`, `Date`,
                   RANK() OVER (ORDER BY `Avg App Rating` DESC) as App_Ranking
            FROM tableCombined
            WHERE `Timestamp` = ? AND `App Name` NOT IN ({}) AND `Total Reviews` >= ?
        ) ranked_apps
        WHERE `App Name` = ?
        """.format(
            ",".join(["?"] * len(excludeApps))
        ),
        (timestamp,) + tuple(excludeApps) + (minTotalReviews, app_name),
    )
    resultAppRank = c.fetchone()
    return resultAppRank


# Connect to Database
conn = sqlite3.connect("Database/app_store_stats.db")

# TODO: Refactor which user-selectable filters
app_name = "My Spectrum"
excludeApps = ["Cox App", "Spectrum TV"]
minTotalReviews = 150000

# Get the latest timestamp from the tableCombined
c = conn.cursor()
c.execute("SELECT MAX(`Timestamp`) FROM tableCombined")
latest_timestamp = c.fetchone()[0]

# Pass Values to Parameters
resultAppRank = get_app_stats(
    excludeApps=excludeApps,
    app_name=app_name,
    timestamp=latest_timestamp,
    conn=conn,
    minTotalReviews=minTotalReviews,
)

#! CONTAINER TWO
# Displaying metrics if available
if resultAppRank:
    average_app_rating = resultAppRank[1]
    total_reviews = resultAppRank[2]
    formatted_total_reviews = "{:,}".format(total_reviews)
    app_ranking = resultAppRank[4]
    date = resultAppRank[3]

    with st.container():
        col1, col2, col3, col4, col5 = st.columns([2, 2, 3, 4, 10])
        col1.metric(
            label="App Ranking",
            value=f"#{app_ranking}",
        )
        col2.metric(
            label="App Rating",
            value=float(average_app_rating),
            delta="1.2 °F",
        )
        col3.metric(
            label="Total Reviews",
            value=formatted_total_reviews,
            delta="1.2 °F",
        )
        col4.metric(
            label="Latest Updated",
            value=date,
            delta="1.2 °F",
        )

else:
    st.write(
        f"No data found for the app '{app_name}' with at least 150,000 total reviews on the latest timestamp."
    )

########################################

startDateStr = "2023-06-28 00:00:00"
endDateStr = "2023-07-04 23:59:59"

combinedSQLTable = """
    SELECT *
    FROM tableCombined
"""
combinedData = pd.read_sql_query(combinedSQLTable, conn)

startDate = pd.to_datetime(startDateStr)
endDate = pd.to_datetime(endDateStr)

combinedData["Date"] = pd.to_datetime(combinedData["Date"])
combinedData = combinedData.loc[
    (combinedData["Date"] >= startDate) & (combinedData["Date"] <= endDate)
]

trendRating = combinedData[["Date", "App Name", "Avg App Rating"]]

pivotedData = trendRating.pivot(
    index="Date", columns="App Name", values="Avg App Rating"
)


# Unique App Names
appNames = combinedData["App Name"].unique()
defaultAppFilter = ["My Spectrum", "My Verizon"]


with st.sidebar.expander("Filters"):
    selectApps = st.multiselect("Select Apps", appNames, default=defaultAppFilter)
with st.container():
    filteredData = pivotedData[selectApps]
    st.line_chart(filteredData, use_container_width=True)
conn.close()


# tab1, tab2, tab3, tab4 = st.tabs(
#     ["📊 Combined Ratings", "📱 iOS Ratings", "📱 Android Ratings", "Pivot Table"]
# )

# iOS_file = "iOSratings.xlsx"
# Android_file = "AndroidRatings.xlsx"
# Combined_file = "combinedRatings.xlsx"
# sheet_name = "Sheet1"

# dfCombined = pd.read_excel(Combined_file, sheet_name, usecols="A:I", header=0)
# dfCombined = dfCombined.sort_values(by=["Overall App Rating"], ascending=False)
# dfCombined = dfCombined.reset_index(drop=True)

# dfiOS = pd.read_excel(iOS_file, sheet_name, usecols="B:F", header=0)
# dfiOS = dfiOS.sort_values(by=["iOS App Rating"], ascending=False)
# dfiOS = dfiOS.reset_index(drop=True)
# # styler = dfiOS.style.hide_index()
# # st.write(styler.to_html(), unsafe_allow_html=True)

# dfAndroid = pd.read_excel(Android_file, sheet_name, usecols="B:J", header=0)
# dfAndroid = dfAndroid.sort_values(by=["Android App Rating"], ascending=False)
# dfAndroid = dfAndroid.reset_index(drop=True)

# with tab1:
#     st.header("App Store Ratings")
#     st.dataframe(
#         dfCombined,
#         use_container_width=True,
#         hide_index=True,
#     )

# with tab2:
#     st.header("iOS Store App Rating")
#     st.dataframe(
#         dfiOS,
#         use_container_width=True,
#         hide_index=True,
#     )

# with tab3:
#     st.header("Android Store App Ratings")
#     st.dataframe(
#         dfAndroid,
#         use_container_width=True,
#         hide_index=True,
#     )

# with tab4:
#     st.header("Pivot Table")

#     @st.cache_data()
#     def load_data():
#         return dfCombined

#     dataPivot = load_data()
#     AgGrid(dataPivot, height=400)
