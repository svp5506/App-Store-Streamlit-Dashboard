import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3


st.set_page_config(page_title="App Ratings", layout="wide")

st.title(":blue[My Spectrum App] Insights")


def get_app_ranking(
    exclude_apps=[], app_name="", timestamp="", conn=None, min_total_reviews=150000
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
            ",".join(["?"] * len(exclude_apps))
        ),
        (timestamp,) + tuple(exclude_apps) + (min_total_reviews, app_name),
    )
    resultAppRank = c.fetchone()
    return resultAppRank


conn = sqlite3.connect("Database/app_store_stats.db")

app_name = "My Spectrum"
exclude_apps = ["Cox App", "Spectrum TV"]
min_total_reviews = 150000


with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Get the latest timestamp from the tableCombined
c = conn.cursor()
c.execute("SELECT MAX(`Timestamp`) FROM tableCombined")
latest_timestamp = c.fetchone()[0]

resultAppRank = get_app_ranking(
    exclude_apps=exclude_apps,
    app_name=app_name,
    timestamp=latest_timestamp,
    conn=conn,
    min_total_reviews=min_total_reviews,
)

if resultAppRank:
    average_app_rating = resultAppRank[1]
    total_reviews = resultAppRank[2]
    formatted_total_reviews = "{:,}".format(total_reviews)
    app_ranking = resultAppRank[4]
    date = resultAppRank[3]

    with st.container():
        col1, col2, col3, col4 = st.columns(4)
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
