import pandas as pd

class Utilites1:

    @staticmethod
    def time_to_miliseconds(time_str):
        minutes, sec_ms = time_str.split(':')
        seconds, milliseconds = sec_ms.split('.')

        return (
            int(minutes) * 60 * 1000 +
            int(seconds) * 1000 +
            int(milliseconds)
        )