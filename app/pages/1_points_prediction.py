import streamlit as st
import pandas as pd
import joblib

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Points Prediction",
    page_icon="🏎️",
    layout="wide"
)

# =========================
# LOAD MODEL
# =========================

model = joblib.load("models/model1.pkl")

# =========================
# TITLE
# =========================

st.title("🏎️ Points Prediction")

st.markdown("""
This page predicts whether a Formula 1 driver will score points during the race.
""")

# =========================
# FEATURES
# =========================

FEATURE_ORDER = [
    "round",
    "grid",
    "before_race_points",
    "before_race_position",
    "before_race_wins",
    "before_race_ctor_points",
    "before_race_ctor_position",
    "before_race_ctor_wins",
    "q1_ms",
    "q2_ms",
    "q3_ms",
    "driver_age",
    "quali_round",
    "q3_gap_to_pole",
    "q2_gap_to_pole",
    "drv_avg_finish_last_3",
    "name",
    "race_part_of_day"
]

# =========================
# FRIENDLY FEATURE NAMES
# =========================

FRIENDLY_NAMES = {
    "round": "Race Round",
    "grid": "Starting Grid Position",
    "before_race_points": "Driver Points Before Race",
    "before_race_position": "Driver Championship Position",
    "before_race_wins": "Driver Wins Before Race",
    "before_race_ctor_points": "Constructor Points Before Race",
    "before_race_ctor_position": "Constructor Championship Position",
    "before_race_ctor_wins": "Constructor Wins Before Race",
    "q1_ms": "Q1 Lap Time (ms)",
    "q2_ms": "Q2 Lap Time (ms)",
    "q3_ms": "Q3 Lap Time (ms)",
    "driver_age": "Driver Age",
    "quali_round": "Qualifying Round Reached",
    "q3_gap_to_pole": "Q3 Gap To Pole (ms)",
    "q2_gap_to_pole": "Q2 Gap To Pole (ms)",
    "drv_avg_finish_last_3": "Average Finish Position (Last 3 Races)",
    "name": "Grand Prix Name",
    "race_part_of_day": "Part Of Day"
}

# =========================
# FEATURE TABLE
# =========================

feature_df = pd.DataFrame({
    "Order": range(1, len(FEATURE_ORDER) + 1),
    "Feature": [FRIENDLY_NAMES[f] for f in FEATURE_ORDER]
})

with st.expander("📋 View Expected Feature Order"):

    st.dataframe(
        feature_df,
        use_container_width=True,
        hide_index=True
    )

# =========================
# INPUT SECTION
# =========================

st.subheader("📝 Input Values")

st.markdown("""
Enter values separated by semicolon (`;`) following the displayed feature order.
""")

example_input = (
    "8;6;45;6;0;778;3;0;80344;79962;79820;"
    "20.81;3;933;1010;9.66;Italian Grand Prix;afternoon"
)

user_input = st.text_input(
    "Input",
    value=example_input
)

# =========================
# PREDICTION
# =========================

if st.button("Predict"):

    try:

        values = user_input.split(";")

        # =========================
        # VALIDATION
        # =========================

        if len(values) != len(FEATURE_ORDER):

            st.error(
                f"Expected {len(FEATURE_ORDER)} values, "
                f"but received {len(values)}."
            )

        else:

            # =========================
            # CREATE DATAFRAME
            # =========================

            df = pd.DataFrame([values], columns=FEATURE_ORDER)

            # =========================
            # NUMERIC CONVERSION
            # =========================

            numeric_cols = FEATURE_ORDER[:-2]

            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col])

            # =========================
            # SHOW INPUT DATA
            # =========================

            st.subheader("📊 Parsed Input Data")

            display_df = df.copy()

            display_df.columns = [
                FRIENDLY_NAMES[col]
                for col in display_df.columns
            ]

            st.dataframe(
                display_df,
                use_container_width=True
            )

            # =========================
            # PREDICTION
            # =========================

            prediction = model.predict(df)[0]

            probabilities = model.predict_proba(df)[0]

            # =========================
            # RESULT
            # =========================

            st.subheader("🎯 Prediction Result")

            if prediction == 1:

                st.success(
                    f"Driver WILL score points "
                    f"(Probability: {probabilities[1]:.2%})"
                )

            else:

                st.warning(
                    f"Driver WILL NOT score points "
                    f"(Probability: {probabilities[0]:.2%})"
                )

    except Exception as e:

        st.error(str(e))