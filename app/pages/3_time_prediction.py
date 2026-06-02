import streamlit as st
import pandas as pd
import joblib

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="F1 Lap Time Prediction",
    layout="wide"
)

model = joblib.load('models/model3.pkl')

st.title("F1 Lap Time Predictor")

st.markdown("""
Enter current lap data and telemetry info.

Model will predict the next lap time.
""")

# =========================
# FORM
# =========================

with st.form("prediction_form"):

    # =========================
    # BASIC INFO
    # =========================

    st.subheader("Race Info")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        season = st.number_input("Season", 2020, 2024, 2020)

    with col2:
        round_number = st.number_input("Round", 1, 30, 1)

    with col3:
        event_name = st.selectbox(
            "Event Name", 
            options=[
                'Pre-Season Test 1', 'Pre-Season Test 2', 'Austrian Grand Prix',
                'Styrian Grand Prix', 'Hungarian Grand Prix', 'British Grand Prix',
                '70th Anniversary Grand Prix', 'Spanish Grand Prix',
                'Belgian Grand Prix', 'Italian Grand Prix', 'Tuscan Grand Prix',
                'Russian Grand Prix', 'Eifel Grand Prix', 'Portuguese Grand Prix',
                'Emilia Romagna Grand Prix', 'Turkish Grand Prix',
                'Bahrain Grand Prix', 'Sakhir Grand Prix', 'Abu Dhabi Grand Prix',
                'Pre-Season Test', 'Monaco Grand Prix', 'Azerbaijan Grand Prix',
                'French Grand Prix', 'Dutch Grand Prix',
                'United States Grand Prix', 'Mexico City Grand Prix',
                'São Paulo Grand Prix', 'Qatar Grand Prix',
                'Saudi Arabian Grand Prix', 'Pre-Season Track Session',
                'Australian Grand Prix', 'Miami Grand Prix', 'Canadian Grand Prix',
                'Singapore Grand Prix', 'Japanese Grand Prix',
                'Pre-Season Testing', 'Las Vegas Grand Prix', 'Chinese Grand Prix'
                    ]
       )

    with col4:
        driver = st.selectbox(
            "Driver", 
            options=[
                'ALB', 'BOT', 'GAS', 'GIO', 'GRO', 'HAM', 'KVY', 'LAT', 'LEC',
                'MAG', 'NOR', 'OCO', 'PER', 'RAI', 'RIC', 'RUS', 'SAI', 'STR',
                'VER', 'VET', 'HUL', 'AIT', 'FIT', 'ALO', 'MAZ', 'MSC', 'TSU',
                'KUB', 'ZHO', 'DEV', 'PIA', 'SAR', 'LAW', 'COL', 'BEA'
                    ]
        )

    # =========================
    # LAP DATA
    # =========================

    st.subheader("Lap Information")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        lap_number = st.number_input("Lap Number", min_value=1, value=1)

    with col2:
        stint = st.number_input("Stint", min_value=1, value=1)

    with col3:
        tyre_life = st.number_input("Tyre Life", min_value=0, value=1)

    with col4:
        lap_time_sec = st.number_input(
            "Lap Time (sec)",
            min_value=0.0,
            value=90.0,
            step=0.001
        )

    # =========================
    # SECTORS
    # =========================

    st.subheader("Sector Times")

    col1, col2, col3 = st.columns(3)

    with col1:
        sector1 = st.number_input("Sector 1 (sec)", 0.0, value=30.0)

    with col2:
        sector2 = st.number_input("Sector 2 (sec)", 0.0, value=40.0)

    with col3:
        sector3 = st.number_input("Sector 3 (sec)", 0.0, value=20.0)

    # =========================
    # SPEEDS
    # =========================

    st.subheader("Speed Traps")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        speed_i1 = st.number_input("Speed I1", 0, value=300)

    with col2:
        speed_i2 = st.number_input("Speed I2", 0, value=250)

    with col3:
        speed_fl = st.number_input("Speed FL", 0, value=280)

    with col4:
        speed_st = st.number_input("Speed ST", 0, value=290)

    # =========================
    # TRACK + TYRES
    # =========================

    st.subheader("Track & Tyres")

    col1, col2, col3, col4 = st.columns(4)

     # 1,   12,  124,    4,   41,  412,   24,   21,   14,   45,  451,   51,  167
    with col1:
        track_status = st.number_input("Track Status", value=1)

    with col2:
        compound = st.selectbox(
            "Compound",
            ['SOFT', 'MEDIUM', 'HARD', 'INTERMEDIATE', 'WET']
        )

    with col3:
        team = st.selectbox(
            "Team", 
            options=[
                'Red Bull Racing', 'Mercedes', 'AlphaTauri', 'Alfa Romeo Racing',
                'Haas F1 Team', 'Williams', 'Ferrari', 'McLaren', 'Renault',
                'Racing Point', 'Alpine', 'Aston Martin', 'Alfa Romeo',
                'Kick Sauber', 'RB'
                    ]
       )

    with col4:
        fresh_tyre = st.selectbox(
            "Fresh Tyre",
            [1, 0],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

    # =========================
    # PIT INFO
    # =========================

    st.subheader("Pit Info")

    col1, col2 = st.columns(2)

    # Potrebno proveriti unos i konvertovati u number
    with col1:
        pit_in = st.text_input("Pit In Time (sec)", value="")

    with col2:
        pit_out = st.text_input("Pit Out Time (sec)", value="")

    # =========================
    # SUBMIT
    # =========================

    submit = st.form_submit_button(
        "Predict Next Lap",
        use_container_width=True
    )


# =========================
# ON SUBMIT
# =========================

if submit:
    try:
        
        df_input = pd.DataFrame([{
            "LapTime": lap_time_sec,
            "LapNumber": lap_number,
            "Stint": stint,
            "TyreLife": tyre_life,
            "Sector1Time": sector1,
            "Sector2Time": sector2,
            "Sector3Time": sector3,
            "SpeedI1": speed_i1,
            "SpeedI2": speed_i2,
            "SpeedFL": speed_fl,
            "SpeedST": speed_st,
            "TrackStatus": track_status,
            "Season": season,
            "Round": round_number,
            "LapTime_ms": lap_time_sec * 1000,
            "Driver": driver,
            "Compound": compound,
            "Team": team,
            "FreshTyre": fresh_tyre,
            "EventName": event_name,
            "PitInTime": pit_in,
            "PitOutTime": pit_out
        }])

        # ✅ prikaz unosa
        st.subheader("Input Data")
        st.dataframe(df_input, use_container_width=True)

        # 👉 OVDE ubacuješ svoju logiku
        st.success("✅ Data ready for feature generation and prediction")

    except Exception as e:
        st.error(str(e))