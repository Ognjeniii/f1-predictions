import pandas as pd
import numpy as np

class DB:

    def prepare_data(self, df):
        for col in df.select_dtypes(include=['string', 'boolean']).columns:
            if df[col].dtype.name == 'boolean':
                df[col] = df[col].astype(float)
            else:
                df[col] = df[col].astype(object)

        df = df.replace({pd.NA: np.nan})
        return df
    
    def create_target(self, df):
        df = df.sort_values(
            ['Season', 'Round', 'EventName', 'Driver', 'LapNumber']
        ).copy()

        df['NextPosition'] = (
            df.groupby(
                ['Season', 'Round', 'EventName', 'Driver']
            )['Position']
            .shift(-1)
        )

        mask = df['Position'].notna() & df['NextPosition'].notna()
        df = df[mask].copy()

        df['NextLapProgress'] = np.sign(
            df['Position'] - df['NextPosition']
        )

        return df
    
    def get_data(self):
        df = pd.read_csv('../data/Model2/laps.csv')
        df = self.prepare_data(df)
        df = self.create_target(df)

        return df
