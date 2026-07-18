import datetime
from typing import Optional
from zoneinfo import ZoneInfo
import pandas as pd
import matplotlib.pyplot as plt
import dukascopy_python
import pandas_ta as ta
from dukascopy_python.instruments import *


#CONFIGURATION
class Session:
    def __init__(self, start:datetime.datetime, end:datetime.datetime, start_time:datetime.time, end_time:datetime.time, months:int,starting_balance:int,entry:int,instrument,strategy:str,candle_interval):
        self.start = start
        self.end = end
        self.start_time = start_time
        self.end_time = end_time
        self.months = months
        self.starting_balance=starting_balance
        self.entry=entry
        self.instrument=instrument
        self.strategy=strategy
        self.candle_interval=candle_interval
class Backtest:
    def __init__(self,win_count:int,loss_count:int,break_even_count:int,trade_count:int,total_win_amount:int,total_loss_amount:int,max_drawdown:int,trades_dates:list,trades:list,balance_history:list):
        self.win_count=win_count
        self.loss_count=loss_count
        self.break_even_count=break_even_count
        self.trade_count=trade_count
        self.total_win_amount=total_win_amount
        self.total_loss_amount=total_loss_amount
        self.max_drawdown=max_drawdown
        self.trades_dates=trades_dates
        self.trades=trades
        self.balance_history=balance_history

class InstrumentData:
    def __init__(self,data_5min:pd.DataFrame,data_1hour:pd.DataFrame):
        self.data_5min=data_5min
        self.data_1hour=data_1hour
class Trade:
    def __init__(self,buy_sell:bool,entry_price:float,exit_price:float,entry_datetime:datetime.datetime,exit_datetime:datetime.datetime,entry_amount:float):
        self.buy_sell=buy_sell # 1 BUY, 0 SELL
        self.entry_price=entry_price
        self.exit_price=exit_price
        self.entry_datetime=entry_datetime
        self.exit_datetime=exit_datetime
        self.entry_amount=entry_amount
        self.outcome:float=0
        if(buy_sell==1):
            if(exit_price>entry_price):
                self.win_loss=1 #win 1 loss -1 break_even 0
            elif(exit_price<entry_price):
                self.win_loss=-1
            else:
                self.win_loss=0
            self.outcome=(entry_amount*(exit_price/entry_price))-entry_amount
        elif (buy_sell==0):
            if(exit_price<entry_price):
                self.win_loss=1
            elif(exit_price>entry_price):
                self.win_loss=-1
            else:
                self.win_loss=0
            self.outcome=-((entry_amount*(exit_price/entry_price))-entry_amount)


class Candle:
    def __init__(self,open:float,close:float,high:float,low:float,date:datetime.date,time:datetime.time):
        self.open=open
        self.close=close
        self.high=high
        self.low=low
        self.date=date
        self.time=time
        self.type=(open>close)# green 1 red 0
class OpeningRange:
    def __init__(self,high,low):
        self.high=high
        self.low=low

HOLIDAYS = [
    # New Year
    datetime.datetime(2024, 1, 1).date(),
    datetime.datetime(2025, 1, 1).date(),

    # Martin Luther King Jr Day (US)
    datetime.datetime(2024, 1, 15).date(),
    datetime.datetime(2025, 1, 20).date(),

    # Presidents' Day (US)
    datetime.datetime(2024, 2, 19).date(),
    datetime.datetime(2025, 2, 17).date(),

    # Good Friday
    datetime.datetime(2024, 3, 29).date(),
    datetime.datetime(2025, 4, 18).date(),

    # Easter Monday (Europe/UK)
    datetime.datetime(2024, 4, 1).date(),
    datetime.datetime(2025, 4, 21).date(),

    # Early May Bank Holiday (UK)
    datetime.datetime(2024, 5, 6).date(),
    datetime.datetime(2025, 5, 5).date(),

    # Memorial Day (US)
    datetime.datetime(2024, 5, 27).date(),
    datetime.datetime(2025, 5, 26).date(),

    # US Independence Day
    datetime.datetime(2024, 7, 4).date(),
    datetime.datetime(2025, 7, 4).date(),

    # Summer Bank Holiday (UK)
    datetime.datetime(2024, 8, 26).date(),
    datetime.datetime(2025, 8, 25).date(),

    # Labor Day (US)
    datetime.datetime(2024, 9, 2).date(),
    datetime.datetime(2025, 9, 1).date(),

    # Thanksgiving (US)
    datetime.datetime(2024, 11, 28).date(),
    datetime.datetime(2025, 11, 27).date(),

    # Christmas Day
    datetime.datetime(2024, 12, 25).date(),
    datetime.datetime(2025, 12, 25).date(),
]
#START and END of BACKTEST
def setupSession()->Optional[Session]:
    try:
        string_start_date= input("Enter session start date (DD.MM.YYYY): ")
        START_DATE= datetime.datetime.strptime(string_start_date, "%d.%m.%Y")
        string_end_date= input("Enter session end date (DD.MM.YYYY): ")
        END_DATE= datetime.datetime.strptime(string_end_date, "%d.%m.%Y")

        MONTHS = (END_DATE.year - START_DATE.year) * 12 + (END_DATE.month - START_DATE.month)

        string_start_time= input("Enter session start time (HH:MM): ")
        SESSION_STARTTIME=datetime.datetime.strptime(string_start_time,"%H:%M").time()
        string_end_time= input("Enter session end time (HH:MM): ")
        SESSION_ENDTIME=datetime.datetime.strptime(string_end_time,"%H:%M").time()



    except ValueError:
        print("Invalid Datetime Format")
        return
    try:
        STARTING_BALANCE=int(input("Input starting balance: $"))
        ENTRY=int(input("Input entry amount per trade: $"))
        INSTRUMENT=INSTRUMENT_US_TECH_US_USD

    except ValueError:
        print("Wrong Value")
        return
    try:
        SESSION = Session(
        start=START_DATE,
        end=END_DATE,
        start_time=SESSION_STARTTIME,
        end_time=SESSION_ENDTIME,
        months=MONTHS,
        starting_balance=STARTING_BALANCE,
        entry=ENTRY,
        instrument=INSTRUMENT,
        strategy="ORB",
        candle_interval=dukascopy_python.INTERVAL_MIN_5

        )
        return SESSION
    except:
        print("Something went wrong!")
        return
def fetchInstrumentData(SESSION:Session)->Optional[InstrumentData]:
    try:
        SESSION_DATA_5_MIN = dukascopy_python.fetch(
        SESSION.instrument,
        SESSION.candle_interval,
        dukascopy_python.OFFER_SIDE_BID,
        SESSION.start,
        SESSION.end,
        )

        SESSION_DATA_1_HOUR = dukascopy_python.fetch(
        SESSION.instrument,
        dukascopy_python.INTERVAL_HOUR_1,
        dukascopy_python.OFFER_SIDE_BID,
        SESSION.start,
        SESSION.end,
        )
    except:
        print("ERROR: Data couldn't be fetched.")
        return


    return InstrumentData(data_5min=SESSION_DATA_5_MIN, data_1hour=SESSION_DATA_1_HOUR)
def tradeLogic(candle:Candle):
    #LOGIC 1. Check if above EMA 2. Check if VWAP in the way 3. Check if RSI overbought
    index = DF_ACTIVE_PAIR_1_MIN.index.searchsorted(cc.name)+14
    if candle.type==1:#LONG LOGIC
        
    else:#SHORT LOGIC
    

    

def runBacktest(SESSION:Session,INSTRUMENT_DATA:InstrumentData)->Optional[Backtest]:
    test=Backtest(
        win_count=0,
        loss_count=0,
        break_even_count=0,
        trade_count=0,
        total_win_amount=0,
        total_loss_amount=0,
        max_drawdown=0,
        trades_dates=[SESSION.start],
        trades=[],
        balance_history=[SESSION.starting_balance]
    )
    timezone=ZoneInfo("America/New_York")

    DATA_5MIN = INSTRUMENT_DATA.data_5min.tz_convert(timezone)
    DATA_1HOUR = INSTRUMENT_DATA.data_1hour.tz_convert(timezone)

    #SETUP INDICATORS
    DATA_5MIN["rsi"] = ta.rsi(DATA_5MIN["close"], length=14)
    DATA_5MIN["ema_50"] = ta.ema(DATA_5MIN["close"], length=50)
    DATA_5MIN["vwap"] = ta.vwap(DATA_5MIN["high"], DATA_5MIN["low"], DATA_5MIN["close"], DATA_5MIN["volume"])
    DATA_1HOUR["rsi"] = ta.rsi(DATA_1HOUR["close"], length=14)
    DATA_1HOUR["ema_50"] = ta.ema(DATA_1HOUR["close"], length=50)
    DATA_1HOUR["vwap"] = ta.vwap(DATA_1HOUR["high"], DATA_1HOUR["low"], DATA_1HOUR["close"], DATA_1HOUR["volume"])

    candle = DATA_5MIN.iloc[0]
    opening_range_state=False

    for i in range(len(DATA_5MIN)):
        candle=Candle(DATA_5MIN.iloc[i]["open"],DATA_5MIN.iloc[i]["close"],DATA_5MIN.iloc[i]["high"],DATA_5MIN.iloc[i]["low"],DATA_5MIN.iloc[i].name.date(),DATA_5MIN.iloc[i].name.time())
        #Pronadi open
        if candle.time>datetime.time(10,55):
            opening_range_state=False #Close ORB after 1.5h

        elif opening_range_state and candle.time>datetime.time(9,40):
            if candle.high>opening_range.high or candle.low<opening_range.low:
                tradeLogic(candle) 



        if candle.time==datetime.time(9,30): #open candle
            or_candle_1=Candle(DATA_5MIN.iloc[i+1]["open"],DATA_5MIN.iloc[i+1]["close"],DATA_5MIN.iloc[i+1]["high"],DATA_5MIN.iloc[i+1]["low"],DATA_5MIN.iloc[i+1].name.date(),DATA_5MIN.iloc[i+1].name.time())
            or_candle_2=Candle(DATA_5MIN.iloc[i+2]["open"],DATA_5MIN.iloc[i+2]["close"],DATA_5MIN.iloc[i+2]["high"],DATA_5MIN.iloc[i+2]["low"],DATA_5MIN.iloc[i+2].name.date(),DATA_5MIN.iloc[i+2].name.time())
            opening_range=OpeningRange(max(candle.high,or_candle_1.high,or_candle_2.high),min(candle.low,or_candle_1.low,or_candle_2.low))
            opening_range_state=True









#IGNORE HOLIDAYS and SKIP DAYS

def main():
    SESSION=setupSession()
    if (SESSION!=None):
        INSTRUMENT_DATA=fetchInstrumentData(SESSION)
        if (INSTRUMENT_DATA!=None):
            runBacktest(SESSION,INSTRUMENT_DATA)

        else:
            print("Data doesn't exist.")
            return 1
    else:
        print("Session is not defined.")
        return 1
    return 0
if __name__=="__main__":
    main()
