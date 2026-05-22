TRACK_STATUS_BITS = {
            1:  'AllClear',
            2:  'Yellow',
            4:  'SafetyCar',
            8:  'VSC',
            16: 'RedFlag',
            32: 'FormationFlag',
            64: 'SessionEnd'
        }

class FeatureGenerator2:

    @staticmethod
    def status_bits_transformer(track_status):
        return {
            f'Is{name}': int((track_status & bit) > 0)
            for bit, name in TRACK_STATUS_BITS.items()
        }
    
    # gap to driver ahead and follower will user enter manualy

    @staticmethod
    def get_driver_rolling_lap_time(
        df, 
        driver,
        season,
        round_num,
        lap_number,
        window=3,
        driver_col='Driver',
        season_col='Season',
        round_col='Round',
        lap_col='LapNumber',
        laptime_col='LapTime',
        ):
        
        laps = (
            df[
                (df[driver_col] == driver) &
                (df[season_col] == season) &
                (df[round_col] == round_num) &
                (df[lap_col] < lap_number)
            ]
            .sort_values(lap_col)
        )
        
        last_laps = laps[laptime_col].tail(window)

        if len(last_laps) == 0:
            return None
        
        return last_laps.mean()
    
    @staticmethod
    def get_driver_momentum(lap_time, mean_lap_time):
        return lap_time - mean_lap_time