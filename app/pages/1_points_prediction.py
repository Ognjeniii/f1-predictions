import streamlit as st
import pandas as pd
import joblib

from mapping.first_problem.drivers import drivers_list
from mapping.first_problem.constructors import ctor_list
from mapping.first_problem.tracks import track_list

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
    print('Driver: ', driver_id, ' - ', driver_name)

    # =========================
    # CONSTRUCTOR INFO
    # =========================

    st.subheader("Constructor")

    constructor_name = st.selectbox(
        "Constructor",
        options=list(ctor_list.keys())
    )

    ctor_id = ctor_list[constructor_name]
    print('Consturctor: ', ctor_id, ' - ', constructor_name)

    # =========================
    # QUALIFYING TIMES
    # =========================

    st.subheader("Qualifying Times")

    st.markdown("""
    Enter lap times in format: m:ss.ms or in miliseconds.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        q1_ms = st.number_input(
            "Q1 Time (ms)",
            min_value=0
        )

    with col2:
        q2_ms = st.number_input(
            "Q2 Time (ms)",
            min_value=0
        )

    with col3:
        q3_ms = st.number_input(
            "Q3 Time (ms)",
            min_value=0
        )

    # =========================
    # BEST SESSION TIMES
    # =========================

    st.subheader("Best Session Times")

    col1, col2 = st.columns(2)

    with col1:
        best_q2_ms = st.number_input(
            "Best Q2 Time (ms)",
            min_value=0
        )

    with col2:
        best_q3_ms = st.number_input(
            "Best Q3 Time (ms)",
            min_value=0
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
            "q1_ms": q1_ms,
            "q2_ms": q2_ms,
            "q3_ms": q3_ms,
            "best_q2_ms": best_q2_ms,
            "best_q3_ms": best_q3_ms,
            "track": track,
            "race_time": race_time
        }

        raw_df = pd.DataFrame([raw_input_data])

        # =========================
        # DISPLAY INPUT DATA
        # =========================

        st.subheader("📋 Input Summary")

        st.dataframe(
            raw_df,
            use_container_width=True,
            hide_index=True
        )

        # =========================
        # FEATURE ENGINEERING
        # =========================

        # Here you will later:
        #
        # 1. Find driverId
        # 2. Find constructorId
        # 3. Generate historical features
        # 4. Generate gaps
        # 5. Generate averages
        # 6. Create final model input
        #
        # Example:
        #
        # model_input = FeaturePipeline.transform(raw_df)

        # =========================
        # TEMP PLACEHOLDER
        # =========================

        st.info("""
        Feature engineering pipeline will be executed here.
        """)

        # =========================
        # EXAMPLE PREDICTION
        # =========================

        # prediction = model.predict(model_input)[0]
        # probabilities = model.predict_proba(model_input)[0]

        # Temporary fake prediction

        prediction = 1
        probability = 0.82

        # =========================
        # RESULT
        # =========================

        st.subheader("🎯 Prediction Result")

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