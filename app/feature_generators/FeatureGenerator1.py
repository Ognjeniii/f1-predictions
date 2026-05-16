import pandas as pd

# da li svuda napraviti defaultne vrednosti za nazive kolona?
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
    
    # Before applying this method, we must provide df which is merged from races and constructor_standings
    @staticmethod
    def before_race_points_ctor(df, constructorId, year, round):
        previous_races = df[
            (df['constructorId'] == constructorId) &
            (df['year'] == year) &
            (df['round'] < round)                   
        ]

        return previous_races['ctor_points'].iloc[-1]
    
    # Before applying this method, we must provide df which is merged from races and constructor_standings
    @staticmethod
    def before_race_position_ctor(df, constructorId, year, round):
        previous_races = df[
            (df['constructorId'] == constructorId) &
            (df['year'] == year) &
            (df['round'] < round)                   
        ]

        return previous_races['ctor_position'].iloc[-1]
    
    # Before applying this method, we must provide df which is merged from races and constructor_standings
    @staticmethod
    def before_race_wins_ctor(df, constructorId, year, round):
        previous_races = df[
            (df['constructorId'] == constructorId) &
            (df['year'] == year) &
            (df['round'] < round)                   
        ]

        return previous_races['ctor_wins'].iloc[-1]

    # User must enter firstname and lastname, and df here is drivers dataset
    @staticmethod
    def get_driver_age(df, firstname, lastname):
        filtered = df[(
            (df['forename'] == firstname) &
            (df['surname'] == lastname)
        )]

        dob = filtered['dob']
        return (pd.Timestamp.today() - dob).dt.days / 365.25
        
    @staticmethod
    def get_quali_round(q2, q3):
        if q2 is None or q2 == "" or q2 == 0:
            return 1
        if q3 is None or q3 == "" or q3 == 0:
            return 2
        return 3
    
    # User must enter best q3 and q2 times. So, based on that we can calculate gap between current driver.
    @staticmethod
    def calculate_gap_to_pole(driver_time_ms: int, pole_time_ms: int):
        if (
            driver_time_ms is None or
            pole_time_ms is None
        ):
            return None

        return driver_time_ms - pole_time_ms

    # Here, we also need to have positionOrder column, which comes from results dataset
    @staticmethod
    def get_avg_finish(df, year, round, driverId):

        filtered_df = df[
            (df['year'] == year) &
            (df['round'] < round) &
            (df['driverId'] == driverId)
        ]

        filtered_df = filtered_df.sort_values(by=['round'])
        last_races = filtered_df.tail(3)
        if last_races.empty:
            return 0
        
        return last_races['positionOrder'].mean()
    
    @staticmethod
    def get_driver_experience(df, driverId):
        return df.groupby(driverId).cumcount()
    
    @staticmethod
    def get_part_of_day(hour):
        # time = pd.to_datetime(time, format='%H:%M:%S')
        if 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "afternoon"
        else:
            return "evening"