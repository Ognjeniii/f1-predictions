import streamlit as st
import pandas as pd
import joblib
import time
import traceback

from mapping.first_problem.drivers import drivers_list
from mapping.first_problem.constructors import ctor_list
from mapping.first_problem.tracks import track_list

from DB import DB
from feature_generators.FeatureGenerator1 import FeatureGenerator1
from feature_generators.helper_methods.Utilities1 import Utilites1

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="F1 Points Prediction",
    layout="wide"
)

# =========================
# LOAD MODEL
# =========================

model = joblib.load("models/model1.pkl")

# =========================
# TITLE
# =========================

st.title("Formula 1 Points Prediction")

st.markdown("""
Predict whether a Formula 1 driver will score points during the race
based on qualifying and race information.
""")

# =========================
# FORM
# =========================

with st.form("prediction_form"):

    # =========================
    # RACE INFO
    # =========================

    st.subheader("Race Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        year = st.number_input(
            "Season Year",
            min_value=2020,
            max_value=2024,
            value=2020
        )

    with col2:
        round = st.number_input(
            "Race Round",
            min_value=1,
            max_value=30,
            value=1
        )

    with col3:
        grid = st.number_input(
            "Starting Grid Position",
            min_value=1,
            max_value=20,
            value=10
        )

    # =========================
    # DRIVER INFO
    # =========================

    st.subheader("Driver Information")

    driver_name = st.selectbox(
        "Driver",
        options=list(drivers_list.keys())
    )

    driver_id = drivers_list[driver_name]

    # =========================
    # CONSTRUCTOR INFO
    # =========================

    st.subheader("Constructor")

    constructor_name = st.selectbox(
        "Constructor",
        options=list(ctor_list.keys())
    )

    ctor_id = ctor_list[constructor_name]

    # =========================
    # QUALIFYING TIMES
    # =========================

    st.subheader("Qualifying Times")

    st.markdown("""
    Enter lap times in format: m:ss.ms or in miliseconds.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        q1 = st.text_input(
            "Q1 Time (ms)"
        )

    with col2:
        q2 = st.text_input(
            "Q2 Time (ms)"
        )

    with col3:
        q3 = st.text_input(
            "Q3 Time (ms)"
        )

    # =========================
    # BEST SESSION TIMES
    # =========================

    st.subheader("Best Session Times")

    col1, col2 = st.columns(2)

    with col1:
        best_q2 = st.text_input(
            "Best Q2 Time (ms)"
        )

    with col2:
        best_q3 = st.text_input(
            "Best Q3 Time (ms)"
        )

    # =========================
    # TRACK INFO
    # =========================

    st.subheader("Track Information")

    col1, col2 = st.columns(2)

    with col1:
        track = st.selectbox(
            "Grand Prix Name",
            options=list(track_list)
        )

    with col2:
        race_time = st.selectbox(
            "Race Part Of Day",
            options=[
                "morning",
                "afternoon",
                "night"
            ],
            index=1
        )

    # =========================
    # SUBMIT BUTTON
    # =========================

    submit = st.form_submit_button(
        "Predict",
        use_container_width=True
    )

# =========================
# PREDICTION
# =========================

if submit:

    try:

        # =========================
        # CREATE RAW INPUT DATA
        # =========================

        raw_input_data = {
            "year": year,
            "round": round,
            "grid": grid,
            "driver": driver_name,
            "constructor": constructor_name,
            "q1": q1,
            "q2": q2,
            "q3": q3,
            "best_q2": best_q2,
            "best_q3": best_q3,
            "track": track,
            "race_time": race_time
        }

        raw_df = pd.DataFrame([raw_input_data])

        # =========================
        # DISPLAY INPUT DATA
        # =========================

        st.subheader("Input Summary")

        st.dataframe(
            raw_df,
            use_container_width=True,
            hide_index=True
        )

        # =========================
        # FEATURE ENGINEERING
        # =========================

        start = time.perf_counter()

        df = DB.DB.get_data()
        drivers_df = DB.DB.get_drivers()

        # quali
        # round
        before_race_pts = FeatureGenerator1.before_race_points(df, driver_id, year, round)
        before_race_pos = FeatureGenerator1.before_race_position(df, driver_id, year, round)
        before_race_wins = FeatureGenerator1.before_race_wins(df, driver_id, year, round)
        before_race_pts_ctor = FeatureGenerator1.before_race_points_ctor(df, ctor_id, year, round)
        before_race_pos_ctor = FeatureGenerator1.before_race_position_ctor(df, ctor_id, year, round)
        before_race_wins_ctor = FeatureGenerator1.before_race_wins_ctor(df, ctor_id, year, round)
        print('before race features finished')

        # This block need to be checked -----------------------------------
        q1_ms = 0
        q2_ms = 0
        q3_ms = 0

        if ':' not in q3 and '.' not in q3:
            q3_ms = q3
        else:
            q3_ms = Utilites1.time_to_miliseconds(q3)

        if (q2 != 0 and q2 != None) and (':' not in q2 and '.' not in q2):
            q2_ms = q2
        else:
            q2_ms = Utilites1.time_to_miliseconds(q2)
        
        if (q1 != 0 and q1 != None) and (':' not in q1 and '.' not in q1):
            q1_ms = q1
        else:
            q1_ms = Utilites1.time_to_miliseconds(q1)

        # This sub block is for best quali time
        best_q2_ms = 0
        best_q3_ms = 0

        if ':' not in best_q3 and '.' not in best_q3:
            best_q3_ms = best_q3
        else:
            best_q3_ms = Utilites1.time_to_miliseconds(best_q3)

        if ':' not in best_q2 and '.' not in best_q2:
            best_q2_ms = best_q2
        else:
            best_q2_ms = Utilites1.time_to_miliseconds(best_q2)
        # -------------------------------------------------------------------
        print('time converting finished')

        driver_age = FeatureGenerator1.get_driver_age(drivers_df, driver_id)
        print('driver age created')
        quali_round = FeatureGenerator1.get_quali_round(q2, q3)
        print('quali round created')
        q2_gap_to_pole = FeatureGenerator1.calculate_gap_to_pole(q2_ms, best_q2_ms)
        print('gap to q2 pole created')
        q3_gap_to_pole = FeatureGenerator1.calculate_gap_to_pole(q3_ms, best_q3_ms) 
        print('gap to q3 pole created')
        avg_finish = FeatureGenerator1.get_avg_finish(df, year, round, driver_id)  
        # track
        # part_of_day

        end = time.perf_counter()
        print(f'Time taken for generatin features: {end - start:.6f} seconds')

        # =========================
        # PREDICTION
        # =========================

        df_input = pd.DataFrame({
            'round': [round],
            'grid': [grid],
            'before_race_points': [before_race_pts],
            'before_race_position': [before_race_pos],
            'before_race_wins': [before_race_wins],
            'before_race_ctor_points': [before_race_pts_ctor],
            'before_race_ctor_position': [before_race_pos_ctor],
            'before_race_ctor_wins': [before_race_wins_ctor],
            'q1_ms': [q1_ms],
            'q2_ms': [q2_ms],
            'q3_ms': [q3_ms],
            'driver_age': [driver_age],
            'quali_round': [quali_round],
            'q3_gap_to_pole': [q3_gap_to_pole],
            'q2_gap_to_pole': [q2_gap_to_pole],
            'drv_avg_finish_last_3': [avg_finish],
            'name': [track],
            'race_part_of_day': [race_time] 
        })

        print(df_input)

        prediction = model.predict(df_input)
        proba = model.predict_proba(df_input)
        st.write("Classes:", model.classes_)
        st.write("Probabilities:", proba)
        probability = model.predict_proba(df_input)[0][1]

        # =========================
        # RESULT
        # =========================

        st.subheader("Prediction Result")

        if prediction == 1:

            st.success(
                f"""
                Driver WILL score points.
                
                Probability: {probability:.2%}
                """
            )

        else:

            st.warning(
                f"""
                Driver WILL NOT score points.
                
                Probability: {1 - probability:.2%}
                """
            )

    except Exception as e:

        st.error(str(e))
        st.code(traceback.format_exc())
        