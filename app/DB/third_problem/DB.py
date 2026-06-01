import pandas as pd
import numpy as np

class DB:

    @staticmethod
    def get_data():
        df_laps = pd.read_csv('data/Model2/laps.csv').convert_dtypes()

        for col in df_laps.select_dtypes(include=['string', 'boolean']).columns:
            if df_laps[col].dtype.name == 'boolean':
                df_laps[col] = df_laps[col].astype('float')
            else:
                df_laps[col] = df_laps[col].astype('object')

        df_laps = df_laps.replace({pd.NA: np.nan})