class FeatureGenerator1:
    
    # Before applying this method, we must provide df which is merged from races and driver_standings only
    @staticmethod
    def before_race_points(df, driverId, year, round):
        previous_races = df[
            (df['driverId'] == driverId) &
            (df['year'] == year) &
            (df['round'] < round)                   
        ]

        return previous_races['drv_points'].iloc[-1]
    
    # Before applying this method, we must provide df which is merged from races and driver_standings only
    @staticmethod
    def before_race_position(df, driverId, year, round):
        previous_races = df[
            (df['driverId'] == driverId) &
            (df['year'] == year) &
            (df['round'] < round)                   
        ]

        return previous_races['drv_position'].iloc[-1]
    
    # Before applying this method, we must provide df which is merged from races and driver_standings only
    @staticmethod
    def before_race_wins(df, driverId, year, round):
        previous_races = df[
            (df['driverId'] == driverId) &
            (df['year'] == year) &
            (df['round'] < round)                   
        ]

        return previous_races['drv_wins'].iloc[-1]