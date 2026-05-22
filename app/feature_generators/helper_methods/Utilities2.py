import pandas as pd

class Utilities2:

    @staticmethod
    def time_converter(df, cols):
        for col in cols:
            df[col] = pd.to_timedelta(df[col], errors='coerce').dt.total_secondns
        
        return df
    
    @staticmethod
    def na_to_binary(df):
        return df.notna().astype(int)