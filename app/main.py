import streamlit as st
from DB.second_problem.DB import DB

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

# round

# grid

# df = DB.get_data()
# df_drivers = DB.get_drivers()

# points = FeatureGenerator1.before_race_points(df, 1, 2020, 4)
# print('Points for driver id 1: ', points)

# position = FeatureGenerator1.before_race_position(df, 1, 2020, 4)
# print('Position before race:', position)

# wins = FeatureGenerator1.before_race_wins(df, 1, 2020, 4)
# print('Wins before race: ', wins)

# ctor_points = FeatureGenerator1.before_race_points_ctor(df, 131, 2020, 4)
# print('Points for ctor 131: ', ctor_points)

# ctor_position = FeatureGenerator1.before_race_position_ctor(df, 131, 2020, 4)
# print('Position for ctor 131: ', ctor_position)

# ctor_wins = FeatureGenerator1.before_race_wins_ctor(df, 131, 2020, 4)
# print('Wins for ctor 131: ', ctor_wins)

# avg_finish_ham = FeatureGenerator1.get_avg_finish(df, 2020, 4, 1)
# print("Average wins for driver id 1: ", avg_finish_ham)

# q1_ms = Utilites1.time_to_miliseconds('1:04.198')
# q2_ms = Utilites1.time_to_miliseconds('1:03.096')
# q3_ms = Utilites1.time_to_miliseconds('1:02.951')
# print('q1: ', q1_ms, ', q2_ms: ', q2_ms, ' and q3_ms: ', q3_ms)

# driver_age = FeatureGenerator1.get_driver_age(df_drivers, 'Lewis', 'Hamilton')
# print('Lewis age: ', driver_age)

# quali_round = FeatureGenerator1.get_quali_round('neko vreme', '')
# print('Quali round: ', quali_round)

# gap_to_q2_pole = FeatureGenerator1.calculate_gap_to_pole(q2_ms, 63001)
# print('Gap to q2 pole in ms: ', gap_to_q2_pole)

# gap_to_q3_pole = FeatureGenerator1.calculate_gap_to_pole(q3_ms, 62843)
# print('Gap to q3 pole in ms: ', gap_to_q3_pole)

# driver_avg_last_finish = FeatureGenerator1.get_avg_finish(df, 2020, 4, 1)
# print('Avg finish: ', driver_avg_last_finish)

# # track

# race_part_of_day = FeatureGenerator1.get_part_of_day(11)
# print('Part of day: ', race_part_of_day)

# expected input data: round, grid, driver(fname, lname), year, constructor, (q1, q2 and q3 times),
#                      best q2 and q3 times, track, race time



db = DB()
df = db.get_data()

print(df)
 


