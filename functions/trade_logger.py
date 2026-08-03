from classes.Candle import Candle
from classes.Trade import Trade
from classes.Backtest import Backtest
def logTrade(candle:Candle,trade:Trade,test:Backtest):
    trade.exit_date=candle.date
    trade.exit_time=candle.time
    test.trade_count+=1
    test.trades.append(trade)
    test.live_trades.remove(trade)
    outcome=trade.outcome()
    new_balance=test.balance_history[-1] +outcome
    
    if new_balance>test.recent_high:
        test.recent_high=new_balance
    drawdown=((test.recent_high-test.balance_history[-1])/test.recent_high)*100
    if test.max_drawdown<drawdown:
        test.max_drawdown=drawdown

    if trade.win_loss==1:
        test.win_count+=1
        test.total_win_amount+=outcome
    elif trade.win_loss==-1:
        test.loss_count+=1
        test.total_loss_amount+=outcome
    else:
        test.break_even_count+=1

    test.balance_history.append(new_balance)