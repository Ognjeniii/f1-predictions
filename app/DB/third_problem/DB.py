import pandas as pd
import numpy as np

class DB:

    def get_data(self):
        df_laps = pd.read_csv('../data/Model2/laps.csv').convert_dtypes()
        df_laps = self.prepare_data(df_laps)

        return df_laps
    
    def prepare_data(self, df_laps):
        for col in df_laps.select_dtypes(include=['string', 'boolean']).columns:
            if df_laps[col].dtype.name == 'boolean':
                df_laps[col] = df_laps[col].astype('float')
            else:
                df_laps[col] = df_laps[col].astype('object')

        df_laps = df_laps.replace({pd.NA: np.nan})

        df_laps['LapTime'] = pd.to_timedelta(df_laps['LapTime'])
        df_laps['LapTime_ms'] = df_laps['LapTime'].dt.total_seconds() * 1000

        return df_laps