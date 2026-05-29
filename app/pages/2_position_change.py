import streamlit as st

from feature_generators.FeatureGenerator2 import FeatureGenerator2

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="F1 Next Lap Prediction",
    layout="wide"
)

st.title("Position Change Prediction")

st.markdown("""
Enter current lap race information and telemetry data.
The model will predict the next lap performance.
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
        season = st.number_input(
            "Season",
            min_value=2020,
            max_value=2024,
            value=2023
        )

    with col2:
        round_number = st.number_input(
            "Round",
            min_value=1,
            max_value=30,
            value=1
        )

    with col3:
        driver = st.text_input(
            "Driver"
        )

    # =========================
    # CURRENT LAP
    # =========================

    st.subheader("Current Lap")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        lap_number = st.number_input(
            "Lap Number",
            min_value=1,
            value=1
        )

    with col2:
        stint = st.number_input(
            "Stint",
            min_value=1,
            value=1
        )

    with col3:
        tyre_life = st.number_input(
            "Tyre Life", # 0, 1, 2, 3, 4...
            min_value=0,
            value=1
        )

    with col4:
        lap_time = st.number_input(
            "Lap Time (sec)", # 0 days 00:01:15.104000
            min_value=0.0,
            value=90.0,
            step=0.001,
            format="%.3f"
        )

    # =========================
    # TELEMETRY
    # =========================

    st.subheader("Telemetry")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        speed_i1 = st.number_input(
            "Speed I1",
            min_value=0,
            value=300
        )

    with col2:
        speed_i2 = st.number_input(
            "Speed I2",
            min_value=0,
            value=250
        )

    with col3:
        speed_fl = st.number_input(
            "Speed FL",
            min_value=0,
            value=280
        )

    with col4:
        speed_st = st.number_input(
            "Speed ST",
            min_value=0,
            value=290
        )

    # =========================
    # TIMING + TRACK
    # =========================

    st.subheader("Timing and Track Status")

    col1, col2 = st.columns(2)

    with col1:
        lap_start_time = st.number_input(
            "Lap Start Time (sec)", # 0 days 00:32:47.006000
            min_value=0.0,
            value=0.0,
            step=0.1
        )

    with col2:
        track_status = st.number_input(
            "Track Status", # 1,   12,  124,    4,   41,  412,   24,   21,   14,   45,  451,   51,  167
            value=1
        )

    # =========================
    # GAPS
    # =========================

    st.subheader("Race Context")

    col1, col2 = st.columns(2)

    with col1:
        gap_ahead = st.number_input(
            "Gap To Driver Ahead (sec)",
            min_value=0.0,
            value=0.5,
            step=0.001,
            format="%.3f"
        )

    with col2:
        gap_behind = st.number_input(
            "Gap To Driver Behind (sec)",
            min_value=0.0,
            value=0.5,
            step=0.001,
            format="%.3f"
        )

    # =========================
    # TYRES
    # =========================

    st.subheader("Tyres")

    col1, col2 = st.columns(2)

    with col1:
        compound = st.selectbox(
            "Compound",
            options=[
                'SOFT', 'HARD', 'MEDIUM', 'INTERMEDIATE', 'WET', 'UNKNOWN'
            ]
        )

    with col2:
        fresh_tyre = st.selectbox(
            "Fresh Tyre",
            options=[
                1,
                0
            ],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

    # =========================
    # SUBMIT
    # =========================

    submit = st.form_submit_button(
        "Predict Next Lap",
        use_container_width=True
    )

# =========================
# TRACK STATUS ENCODING
# =========================

if submit:

    # LapNumber
    # Stint
    # TyreLife
    # SpeedI1
    # SpeedI2
    # SpeedFL
    # SpeedST
    # LapStartTime
    # TrackStatus
    # IsAllClear
    # IsYellow
    # IsSafetyCar
    # IsVSC
    # IsRedFlag
    # IsFormationFlag
    # IsSessionEnd
    # GapToDriver_Ahead
    # GapToDriver_Behind
    # Driver_LapTime_Mean
    # Driver_Momentum
    # Tyre_Degradation
    # ClosingSpeed_3
    # PaceTrend
    # Compound
    # FreshTyre

    track_statuses = FeatureGenerator2.status_bits_transformer(track_status)

    st.subheader("Input Summary")

    st.write({
        "LapNumber": lap_number,
        "Stint": stint,
        "TyreLife": tyre_life,
        "LapTime": lap_time,
        "SpeedI1": speed_i1,
        "SpeedI2": speed_i2,
        "SpeedFL": speed_fl,
        "SpeedST": speed_st,
        "LapStartTime": lap_start_time,
        "TrackStatus": track_status,
        "IsAllClear": is_all_clear,
        "IsYellow": is_yellow,
        "IsSafetyCar": is_sc,
        "IsVSC": is_vsc,
        "IsRedFlag": is_red,
        "IsFormationFlag": is_formation,
        "IsSessionEnd": is_session_end,
        "GapToDriver_Ahead": gap_ahead,
        "GapToDriver_Behind": gap_behind,
        "Compound": compound,
        "FreshTyre": fresh_tyre
    })