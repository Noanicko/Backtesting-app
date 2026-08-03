import datetime
class Candle:
    def __init__(self,open:float,close:float,high:float,low:float,date:datetime.date,time:datetime.time,rsi:float,vwap:float,ema:float):
        self.open=open
        self.close=close
        self.high=high
        self.low=low
        self.date=date
        self.time=time
        self.datetime=datetime.datetime.combine(date,time)
        self.rsi=rsi
        self.vwap=vwap
        self.ema=ema
        self.type=(open<close)# green 1 red 0
class OpeningRange:
    def __init__(self,high,low):
        self.high=high
        self.low=low