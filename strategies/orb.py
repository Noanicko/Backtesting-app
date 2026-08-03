import datetime
from classes.Candle import Candle
from functions.trade_logger import logTrade
from config import HOLIDAYS
from classes.Session import Session
from classes.Backtest import Backtest
from classes.Trade import Trade
from classes.Candle import OpeningRange
from typing import Optional

#TODO EXIT BREAK_EVEN IF LONGER THAN X
def ORBtradeLogic(candle:Candle,hour_candle:Candle,opening_range:OpeningRange,entry:float)->Optional[Trade]:
    #LOGIC 1. Check if above 1h EMA 2. Check if VWAP in the way 3. Check if RSI overbought
    #index = DF_ACTIVE_PAIR_1_MIN.index.searchsorted(cc.name)+14
    confidence_score=0
    confidence_req=2
    opening_range_size=opening_range.high-opening_range.low
    if (candle.type==1):#LONG LOGIC, has to fit x/3 conditions
        if candle.close>hour_candle.ema:
            confidence_score+=1
        if candle.vwap>(candle.close+opening_range_size) or candle.vwap<candle.close:#VWAP is not in the way
            confidence_score+=1
        if candle.rsi<70:
            confidence_score+=1
        if confidence_score>=confidence_req:
            #enter_trade
            return Trade(1,candle.close,None,candle.date,candle.time,None,None,entry,candle.close+opening_range_size,candle.close-opening_range_size)
    else:#SHORT LOGIC
        if candle.close<hour_candle.ema:
            confidence_score+=1
        if candle.vwap<(candle.close-opening_range_size) or candle.vwap>candle.close:#VWAP is not in the way
            confidence_score+=1
        if candle.rsi>30:
            confidence_score+=1
        if confidence_score>=confidence_req:
            #enter_trade
            return Trade(0,candle.close,None,candle.date,candle.time,None,None,entry,candle.close-opening_range_size,candle.close+opening_range_size)
    return

def ORB_logic(DATA_5MIN,DATA_1HOUR,SESSION:Session,test:Backtest):
    recent_high=test.balance_history[0]
    opening_range_state=False
    for i in range(len(DATA_5MIN)):
            candle=Candle(DATA_5MIN.iloc[i]["open"],DATA_5MIN.iloc[i]["close"],DATA_5MIN.iloc[i]["high"],DATA_5MIN.iloc[i]["low"],DATA_5MIN.iloc[i].name.date(),DATA_5MIN.iloc[i].name.time(),DATA_5MIN.iloc[i]["rsi"],DATA_5MIN.iloc[i]["vwap"],DATA_5MIN.iloc[i]["ema_50"])
            hour_idx = DATA_1HOUR.index.searchsorted(DATA_5MIN.iloc[i].name, side="right") - 1 #Current Hour 
            hour_candle = Candle(DATA_1HOUR.iloc[hour_idx]["open"],DATA_1HOUR.iloc[hour_idx]["close"],DATA_1HOUR.iloc[hour_idx]["high"],DATA_1HOUR.iloc[hour_idx]["low"],DATA_1HOUR.iloc[hour_idx].name.date(),DATA_1HOUR.iloc[hour_idx].name.time(),DATA_1HOUR.iloc[hour_idx]["rsi"],DATA_1HOUR.iloc[hour_idx]["vwap"],DATA_1HOUR.iloc[hour_idx]["ema_50"])
            if candle.date in HOLIDAYS:
                continue
            #Pronadi open #ORB Stragegy logic
            if test.live_trades:
                trade:Trade
                for trade in test.live_trades[:]:
                    #TODO:Trade Timeout
                    TIMEOUT_HOURS=3
                    TIMEOUT_MINUTES=0
                    TIMEOUT_SECONDS=0
                    BREAKEVEN_HOURS=2
                    BREAKEVEN_MINUTES=0
                    BREAKEVEN_SECONDS=0

                    #EXIT AFTER 2 HOURS IF PRICE TOUCHES ENTRY PRICE
                    if candle.datetime-trade.entry_datetime>datetime.timedelta(hours=BREAKEVEN_HOURS,minutes=BREAKEVEN_MINUTES,seconds=BREAKEVEN_SECONDS) and (candle.low<=trade.entry_price and candle.high>=trade.entry_price):
                        trade.exit_price=trade.entry_price
                        logTrade(candle,trade,test)

                    #EXIT AFTER 3 HOURS, TIMEOUT
                    elif candle.datetime-trade.entry_datetime>datetime.timedelta(hours=TIMEOUT_HOURS,minutes=TIMEOUT_MINUTES,seconds=TIMEOUT_SECONDS):
                        trade.exit_price=candle.close
                        logTrade(candle,trade,test)
                    #BUY Logic
                    elif trade.buy_sell==1:
                        if trade.TP<=candle.high:#WIN
                            trade.exit_price=trade.TP
                            logTrade(candle,trade,test)

                        elif trade.SL>=candle.low:#LOSE
                            trade.exit_price=trade.SL
                            logTrade(candle,trade,test)
                        
                    #SELL Logic
                    elif trade.buy_sell==0:
                        if trade.TP>=candle.low:#WIN
                            trade.exit_price=trade.TP
                            logTrade(candle,trade,test)

                        elif trade.SL<=candle.high:#LOSE
                            trade.exit_price=trade.SL
                            logTrade(candle,trade,test)
                
            if candle.time>datetime.time(10,55):
                opening_range_state=False #Close ORB after 1.5h\
            
            elif candle.time==datetime.time(9,30): #open candle
                or_candle_1=Candle(DATA_5MIN.iloc[i+1]["open"],DATA_5MIN.iloc[i+1]["close"],DATA_5MIN.iloc[i+1]["high"],DATA_5MIN.iloc[i+1]["low"],DATA_5MIN.iloc[i+1].name.date(),DATA_5MIN.iloc[i+1].name.time(),DATA_5MIN.iloc[i+1]["rsi"],DATA_5MIN.iloc[i+1]["vwap"],DATA_5MIN.iloc[i+1]["ema_50"])
                or_candle_2=Candle(DATA_5MIN.iloc[i+2]["open"],DATA_5MIN.iloc[i+2]["close"],DATA_5MIN.iloc[i+2]["high"],DATA_5MIN.iloc[i+2]["low"],DATA_5MIN.iloc[i+2].name.date(),DATA_5MIN.iloc[i+2].name.time(),DATA_5MIN.iloc[i+2]["rsi"],DATA_5MIN.iloc[i+2]["vwap"],DATA_5MIN.iloc[i+2]["ema_50"])
                opening_range=OpeningRange(max(candle.high,or_candle_1.high,or_candle_2.high),min(candle.low,or_candle_1.low,or_candle_2.low)) #Form the opening range using the first 3 5-minute candles
                opening_range_state=True #Opening range formed

            elif opening_range_state and candle.time>datetime.time(9,40): #Conditions to enter a trade after 9:45
                if candle.close>opening_range.high or candle.close<opening_range.low:
                    newTrade=ORBtradeLogic(candle,hour_candle,opening_range,SESSION.entry)
                    if newTrade!=None:
                        opening_range_state=False #Turn off entries after trade entry
                        test.live_trades.append(newTrade) #ADD a live trade to the list
