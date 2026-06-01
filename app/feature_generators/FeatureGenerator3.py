import pandas as pd

class FeatureGenerator3:

    # Method that retrieves previous lap time for driver, if lap_number is 0, returns current lap time. 
    # If there is no laps for input data - None.
    @staticmethod
    def get_prev_lap_ms(df, season, event_name, driver, lap_number):

        prev_lap = lap_number - 1

        result = df.loc[
            (df['Season'] == season) &
            (df['EventName'] == event_name) &
            (df['Driver'] == driver) &
            (df['LapNumber'] == prev_lap),
            'LapTime'
        ]

        if not result.empty:
            return result.iloc[0]

        current_result = df.loc[
            (df['Season'] == season) &
            (df['EventName'] == event_name) &
            (df['Driver'] == driver) &
            (df['LapNumber'] == lap_number),
            'LapTime'
        ]

        return current_result.iloc[0] if not current_result.empty else None

    # Method that returns difference between previous and current lap.
    @staticmethod
    def get_lap_delta(lap_time_ms, prev_lap_time_ms):
        return lap_time_ms - prev_lap_time_ms

    @staticmethod
    def get_rolling_pace(df, season, event_name, driver, lap_number):
        laps = df.loc[
            (df['Season'] == season) &
            (df['EventName'] == event_name) &
            (df['Driver'] == driver) &
            (df['LapNumber'] <= lap_number),
            ['LapNumber', 'LapTime_ms']
            .sort_values('LapNumber')
        ]

        last_3 = laps.tail(3)['LapTime_ms']

        if len(last_3) == 0:
            current = df.loc[
                (df['Season'] == season) &
                (df['EventName'] == event_name) &
                (df['Driver'] == driver) &
                (df['LapNumber'] == lap_number),
                'LapTime_ms'
            ]
            return current.iloc[0] if not current.empty else None
        return last_3.mean()
    
    # Method that we use to get realtive pace of driver - drivers time - mean time for all drivers.
    @staticmethod
    def get_relative_pace(df, season, round, lap_number, curr_lap_time):
        lap_mean = df.loc(
            (df['Season'] == season) &
            (df['Round'] == round) &
            (df['LapNumber'] == lap_number),
            'LapTime_ms'
        ).mean()

        if pd.isna(lap_mean):
            return 0
        
        return curr_lap_time - lap_mean
    
    # In this method we are generation feature for tyre life.
    @staticmethod
    def get_stint_phase(tyre_life):
        if tyre_life <= 5:
            return 0   # fresh
        elif tyre_life <= 15:
            return 1   # mid
        else:
            return 2   # worn