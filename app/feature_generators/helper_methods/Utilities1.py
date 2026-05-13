import pandas as pd

class Utilites1:

    @staticmethod
    def time_to_miliseconds(time_str):
        minutes, seconds = time_str.split(':')
        seconds, milliseconds = time_str.split('.')

        return (
            int(minutes) * 60 * 1000 +
            int(seconds) * 1000 +
            int(milliseconds)
        )
    
    @staticmethod
    def get_driver_dob(df, firstname, lastname):
        filtered = df[(
            (df['forename'] == firstname) &
            (df['surename'] == lastname)
        )]
    
