import pandas as pd

class DB:
    
    @staticmethod
    def get_data():
        races_df = pd.read_csv('../data/races.csv')
        driver_standings_df = pd.read_csv('../data/driver_standings.csv')
        constructor_standings_df = pd.read_csv('../data/constructor_standings.csv')
        drivers_df = pd.read_csv('../data/drivers.csv')
        qualifying_df = pd.read_csv('../data/qualifying.csv')
        status_df = pd.read_csv('../data/status.csv')

        races_df = races_df[races_df['raceId'] >= 1031]
        cols = ['raceId', 'circuitId', 'year', 'round', 'name', 'date', 'time']
        races_df = races_df[cols]

        df = races_df.merge(qualifying_df, on='raceId', how='left')

        df['grid'] = df['position']
        df = df.drop(columns='position')

        driver_standings_df = driver_standings_df.rename(columns={
            'points': 'drv_points',
            'position': 'drv_position',
            'positionText': 'drv_position_text',
            'wins': 'drv_wins',
        })

        constructor_standings_df = constructor_standings_df.rename(columns={
            'points': 'ctor_points',
            'position': 'ctor_position',
            'positionText': 'ctor_position_text',
            'wins': 'ctor_wins',
        })
            
        df = df.merge(driver_standings_df, on=['raceId', 'driverId'], how='left')
        df = df.merge(constructor_standings_df, on=['raceId', 'constructorId'], how='left')

        drivers_red = drivers_df[['driverId', 'dob']]
        df = df.merge(drivers_red, on='driverId', how='left')

        return df