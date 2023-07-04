import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# from st_aggrid import AgGrid


def get_app_ranking(app_name, date, conn, min_total_reviews=150000):
    c = conn.cursor()
    c.execute(
        """
        SELECT `App Name`, `Avg App Rating`, `Total Reviews`, App_Ranking
        FROM (
            SELECT `App Name`, `Avg App Rating`, `Total Reviews`,
                   RANK() OVER (ORDER BY `Avg App Rating` DESC) as App_Ranking
            FROM tableCombined
            WHERE `Date` = ?
        ) ranked_apps
        WHERE `App Name` = ? AND `Total Reviews` >= ?
        """,
        (date, app_name, min_total_reviews),
    )
    result = c.fetchone()
    return result


conn = sqlite3.connect("Database/app_store_stats.db")

app_name = "My Spectrum"

st.set_page_config(page_title="App Ratings", layout="wide")


with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Get the latest date from the tableCombined
c = conn.cursor()
c.execute("SELECT MAX(`Date`) FROM tableCombined")
latest_date = c.fetchone()[0]

result = get_app_ranking(app_name, latest_date, conn)

if result:
    average_app_rating = result[1]
    total_reviews = result[2]
    formatted_total_reviews = "{:,}".format(total_reviews)
    app_ranking = result[3]

    with st.container():
        col1, col2, col3 = st.columns(3)
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

else:
    st.write(
        f"No data found for the app '{app_name}' with at least 150,000 total reviews on the latest date."
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
