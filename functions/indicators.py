import pandas_ta as ta
def apply_indicators(data5,data1):
    data5["rsi"] = ta.rsi(data5["close"], length=14)
    data5["ema_50"] = ta.ema(data5["close"], length=50)
    data5["vwap"] = ta.vwap(data5["high"], data5["low"], data5["close"], data5["volume"])
    data1["rsi"] = ta.rsi(data1["close"], length=14)
    data1["ema_50"] = ta.ema(data1["close"], length=50)
    data1["vwap"] = ta.vwap(data1["high"], data1["low"], data1["close"], data1["volume"])