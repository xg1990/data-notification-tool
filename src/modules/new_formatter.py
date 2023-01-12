import pandas as pd

class TimeStringFormatter:
    @staticmethod
    def format(msg):
        for k, v in msg.items():
            if isinstance(v, pd.Timestamp):
                msg[k] = v.strftime("%Y-%m-%d %H:%M:%S")
        return str(msg.message)
