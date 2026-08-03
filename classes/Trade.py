import datetime
from typing import Optional
class Trade:
    def __init__(self,buy_sell:bool,entry_price:float,exit_price:Optional[float],entry_date:datetime.date,entry_time:datetime.time,exit_date:Optional[datetime.date],exit_time:Optional[datetime.time],entry_amount:float,TP:float,SL:float):
        self.buy_sell=buy_sell # 1 BUY, 0 SELL
        self.entry_price=entry_price
        self.exit_price=exit_price
        self.entry_date=entry_date
        self.entry_time=entry_time
        self.exit_date=exit_date
        self.exit_time=exit_time
        self.entry_amount=entry_amount
        self.TP=TP
        self.SL=SL
        self.entry_datetime=datetime.datetime.combine(entry_date,entry_time)

    def outcome(self):
        progress = min(abs(self.exit_price - self.entry_price) /abs(self.TP - self.entry_price),1.0)
        if self.exit_price is None:
            return None
        else:
            if(self.buy_sell==1):
                if(self.exit_price>self.entry_price):
                    self.win_loss=1 #win 1 loss -1 break_even 0
                    return (self.entry_amount*progress)
                elif(self.exit_price<self.entry_price):
                    self.win_loss=-1
                    return -(self.entry_amount*progress)
                else:
                    self.win_loss=0
                    return 0
                #TODO return (self.entry_amount*(self.exit_price/self.entry_price))-self.entry_amount
                
            elif (self.buy_sell==0):
                if(self.exit_price<self.entry_price):
                    self.win_loss=1
                    return (self.entry_amount*progress)
                elif(self.exit_price>self.entry_price):
                    self.win_loss=-1
                    return -(self.entry_amount*progress)
                else:
                    self.win_loss=0
                    return 0
                #TODO return -((self.entry_amount*(self.exit_price/self.entry_price))-self.entry_amount)