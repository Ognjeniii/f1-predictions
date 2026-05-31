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
    
    # gap to driver ahead and follower will user enter manually

    # Method that returns mean lap time for given driver, season...
    @staticmethod
    def get_driver_rolling_lap_time(
        df, 
        driver,
        season,
        round_num,
        lap_number,
        curr_lap_time,
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
            return curr_lap_time
        
        return last_laps.mean()
    
    # Method that returns drivers momentum - how much driver is actually faster
    @staticmethod
    def get_driver_momentum(lap_time, mean_lap_time):
        return lap_time - mean_lap_time

    # ================== helper methods for closing speed ==================
    @staticmethod
    def create_gap_ahead(df, season, race, lap):
        df = df.copy()

        df = df[
            (df['Season'] == season) &
            (df['EventName'] == race) &
            (df['LapNumber'] <= lap)
        ].sort_values(['EventName', 'LapNumber', 'Position'])

        grp = df.groupby(['EventName', 'LapNumber'])

        df['AheadLapStartTime'] = (
            grp['LapStartTime']
            .shift(1)
        )

        df['GapAhead'] = (
            df['LapStartTime'] - df['AheadLapStartTime']
        )

        return df

    @staticmethod
    def get_closing_speed(df, season, race, driver, lap_number, window=3):
        df = FeatureGenerator2.create_gap_ahead(df, season, race, lap_number)

        drv = (
            df[
                (df['Season'] == season) &
                (df['EventName'] == race) &
                (df['Driver'] == driver) &
                (df['LapNumber'] <= lap_number)
            ]
            .sort_values('LapNumber')
            .copy()
        )

        drv['_prev_gap'] = (
            drv['GapAhead']
            .shift(1)
        )

        drv['closing_speed'] = (
            drv['_prev_gap'] - drv['GapAhead']
        )

        return (
            drv['closing_speed']
            .rolling(window=window, min_periods=1)
            .mean()
            .iloc[-1]
        )

    # =================================================================

    # Method that use previous laps to find do driver going faster or not - NE RADI
    @staticmethod
    def get_pace_trend(
        df,
        season,
        race,
        driver,
        lap_number,
        window=3
    ):
        df = df.copy()

        driver_df = (
            df[
                (df['Season'] == season) &
                (df['EventName'] == race) &
                (df['Driver'] == driver) &
                (df['LapNumber'] <= lap_number)
            ]
            .sort_values('LapNumber')
        )

        if len(driver_df) == 0:
            return 0

        driver_df['roll_mean'] = (
            driver_df['LapTime']
            .rolling(window=window, min_periods=1)
            .mean()
        )

        driver_df['prev_roll_mean'] = driver_df['roll_mean'].shift(window)
        driver_df['pace_trend'] = driver_df['roll_mean'] - driver_df['prev_roll_mean']

        return driver_df['pace_trend'].iloc[-1]
    
    # Method that we use to find how old tyres are.
    @staticmethod
    def get_tyre_degradation(
        df, 
        season, 
        race,
        driver,
        lap_number,
        window=3
    ):
        drv = (
            df[
                (df['Season'] == season) &
                (df['EventName'] == race) &
                (df['Driver'] == driver) &
                (df['LapNumber'] <= lap_number)
            ]
            .copy()
        )

        if drv.empty:
            return None
        
        drv = drv.sort_values(['Stint', 'TyreLife'])

        drv['TyreDegradation'] = (
            drv
            .groupby('Stint')['LapTime']
            .rolling(window=window, min_periods=2)
            .mean()
            .shift(1)
            .reset_index(level=0, drop=True)
        )

        drv['TyreDegradation'] = (
            drv['TyreDegradation']
            .fillna(drv['LapTime'])
        )

        return drv['TyreDegradation'].iloc[-1]