import pandas as pd
class FeatureGenerator1:
    
    # Before applying this method, we must provide df which is merged from races and driver_standings
    @staticmethod
    def before_race_points(df, driverId, year, round):
        previous_races = df[
            (df['driverId'] == driverId) &
            (df['year'] == year) &
            (df['round'] < round)                   
        ]

        return previous_races['drv_points'].iloc[-1]
    
    # Before applying this method, we must provide df which is merged from races and driver_standings
    @staticmethod
    def before_race_position(df, driverId, year, round):
        previous_races = df[
            (df['driverId'] == driverId) &
            (df['year'] == year) &
            (df['round'] < round)                   
        ]

        return previous_races['drv_position'].iloc[-1]
    
    # Before applying this method, we must provide df which is merged from races and driver_standings
    @staticmethod
    def before_race_wins(df, driverId, year, round):
        previous_races = df[
            (df['driverId'] == driverId) &
            (df['year'] == year) &
            (df['round'] < round)                   
        ]

        return previous_races['drv_wins'].iloc[-1]

    # User must enter firstname and lastname
    @staticmethod
    def get_driver_age(df, firstname, lastname):
        filtered = df[(
            (df['forename'] == firstname) &
            (df['surname'] == lastname)
        )]

        dob = filtered['dob']
        return (pd.Timestamp.today() - dob).dt.days / 365.25
    
    @staticmethod
    def get_part_of_day(hour):
        # time = pd.to_datetime(time, format='%H:%M:%S')
        if 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "afternoon"
        else:
            return "evening"
        
    @staticmethod
    def get_quali_round(q1, q2, q3):

        if q2 is None or q2 == "" or q2 == 0:
            return 1
        if q3 is None or q3 == "" or q3 == 0:
            return 2
        return 3
    
    # User must enter best q3 and q2 times. So, based on that we can calculate gap between current driver.
    @staticmethod
    def calculate_gap_to_pole(driver_time_ms, pole_time_ms):

        if (
            driver_time_ms is None or
            pole_time_ms is None
        ):
            return None

        return driver_time_ms - pole_time_ms