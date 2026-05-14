import streamlit as st
import pandas as pd
from feature_generators.FeatureGenerator1 import FeatureGenerator1
from DB.DB import DB

# st.set_page_config(
#     page_title="F1 Prediction System",
#     layout="wide"
# )

# st.title("F1 Prediction System")

# st.write("""
# This application demonstrates three machine learning problems:

# 1. Driver points prediction
# 2. Position change prediction
# 3. Next lap time prediction
# """)

# st.info("Choose a page from the sidebar.")

# ==========================================================================

df = DB.get_data()
print(df)
# points = FeatureGenerator1.before_race_points(df, 830, 2020, 5)
# print(points)

avg_finish_ham = FeatureGenerator1.get_avg_finish(df, 2020, 4, 1)
print("Average wins: ", avg_finish_ham)


