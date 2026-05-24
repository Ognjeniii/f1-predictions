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
    
    # Method that returns drivers momentum - how much driver is actually faster
    @staticmethod
    def get_driver_momentum(lap_time, mean_lap_time):
        return lap_time - mean_lap_time

    # ================== helper methods for closing speed ==================
    # @staticmethod
    # def add_cumulative_time(
    #     df,
    #     season_col='Season',
    #     race_col='EventName',
    #     driver_col='Driver',
    #     lap_col='LapNumber',
    #     time_col='LapTime'
    # ):
    #     df = df.copy()

    #     df = df.sort_values(
    #         [season_col, race_col, driver_col, lap_col]
    #     )

    #     df['CumRaceTime'] = (
    #         df.groupby(
    #             [season_col, race_col, driver_col]
    #         )[time_col]
    #         .cumsum()
    #     )

    #     return df

    # @staticmethod
    # def get_gap_to_ahead(
    #     df,
    #     season,
    #     race,
    #     lap_number,
    #     driver,
    #     season_col='Season',
    #     race_col='EventName',
    #     lap_col='LapNumber',
    #     driver_col='Driver',
    #     time_col='LapTime',
    #     position_col='Position'
    # ):

    #     # filtriraj samo potrebnu trku i lap
    #     lap_df = (
    #         df[
    #             (df[season_col] == season) &
    #             (df[race_col] == race) &
    #             (df[lap_col] == lap_number)
    #         ]
    #         .copy()
    #         .sort_values(position_col)
    #         .reset_index(drop=True)
    #     )

    #     # kumulativno vreme lokalno (bez menjanja originalnog df)
    #     lap_df['CumRaceTime'] = (
    #         lap_df
    #         .sort_values(position_col)[time_col]
    #         .cumsum()
    #     )

    #     lap_df['gap_to_ahead'] = (
    #         lap_df['CumRaceTime']
    #         - lap_df['CumRaceTime'].shift(1)
    #     )

    #     row = lap_df[
    #         lap_df[driver_col] == driver
    #     ]

    #     if row.empty:
    #         return None

    #     return row['gap_to_ahead'].iloc[0]
    

    # @staticmethod
    # def get_closing_speed_live(
    #     df,
    #     season,
    #     race,
    #     driver,
    #     lap_number,
    #     window=3
    # ):

    #     gaps = []

    #     # isto kao history u transformeru
    #     for lap in range(1, lap_number + 1):

    #         gap = FeatureGenerator2.get_gap_to_ahead(
    #             df,
    #             season,
    #             race,
    #             lap,
    #             driver
    #         )

    #         gaps.append(gap)

    #     # pandas shift(1)
    #     closing_speeds = []

    #     for i in range(1, len(gaps)):

    #         prev_gap = gaps[i - 1]
    #         curr_gap = gaps[i]

    #         if prev_gap is None or curr_gap is None:
    #             closing_speeds.append(None)
    #         else:
    #             closing_speeds.append(
    #                 prev_gap - curr_gap
    #             )

    #     # pandas rolling(window).mean()
    #     valid = [
    #         x for x in closing_speeds[-window:]
    #         if x is not None
    #     ]

    #     if len(valid) < window:
    #         return None

    #     return sum(valid) / window
    # =================================================================

    # Method that use previous laps to find do driver going faster or not - NE RADI
    @staticmethod
    def get_pace_trend(
        df,
        season,
        race,
        driver,
        lap_number,
        window=3,
        season_col='Season',
        race_col='EventName',
        driver_col='Driver',
        lap_col='LapNumber',
        laptime_col='LapTime'
    ):

        driver_df = (
            df[
                (df[season_col] == season) &
                (df[race_col] == race) &
                (df[driver_col] == driver) &
                (df[lap_col] <= lap_number)
            ]
            .sort_values(lap_col)
        )

        laps = driver_df[laptime_col].tolist()

        if len(laps) < window + 1:
            return None

        rolling_means = []
        for i in range(len(laps) - window + 1):
            rolling_means.append(
                sum(laps[i:i+window]) / window
            )

        last = rolling_means[-1]
        prev = rolling_means[-1 - window]

        return last - prev