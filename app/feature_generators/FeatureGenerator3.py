import pandas as pd

class FeatureGenerator3:

    # Method that retrieves previous lap time for driver, if lap_number is 0, returns current lap time. If there is no laps for input data - None.
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
    def get_rolling_pace(df, season, event_name, driver, lap_time_ms):
        