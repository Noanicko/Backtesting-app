import pandas as pd
class InstrumentData:
    def __init__(self,data_5min:pd.DataFrame,data_1hour:pd.DataFrame):
        self.data_5min=data_5min
        self.data_1hour=data_1hour