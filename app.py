import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid
import sqlite3


conn = sqlite3.connect("Database/app_store_stats.db")
print("Database Accessed")

c = conn.cursor()
c.execute(
    "SELECT AVG(`Avg App Rating`) FROM tableCombined WHERE `App Name` = 'My Spectrum' AND `Date` = (SELECT MAX(`Date`) FROM tableCombined)"
)

appRatingMSA = c.fetchone()

st.set_page_config(page_title="App Ratings", layout="wide")

st.metric(label="My Spectrum App", value=float(appRatingMSA[0]), delta="1.2 °F")


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
