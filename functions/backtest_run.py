from classes.Backtest import Backtest
from classes.Session import Session
from classes.InstrumentData import InstrumentData
from zoneinfo import ZoneInfo
from typing import Optional
from functions.indicators import apply_indicators
from strategies.orb import ORB_logic

def runBacktest(SESSION:Session,INSTRUMENT_DATA:InstrumentData)->Optional[Backtest]:
    test=Backtest(trades_dates=[SESSION.start], balance_history=[SESSION.starting_balance],recent_high=SESSION.starting_balance)

    timezone=ZoneInfo("America/New_York")

    DATA_5MIN = INSTRUMENT_DATA.data_5min.tz_convert(timezone)
    DATA_1HOUR = INSTRUMENT_DATA.data_1hour.tz_convert(timezone)
    apply_indicators(DATA_5MIN,DATA_1HOUR)
    
    if SESSION.strategy=="ORB":
        ORB_logic(DATA_5MIN,DATA_1HOUR,SESSION,test)

    print(f"Requested: {SESSION.start} -> {SESSION.end}")
    print(f"Received : {DATA_5MIN.index.min()} -> {DATA_5MIN.index.max()}")
    test.print_summary()
    test.draw_graph()