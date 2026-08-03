import datetime
from typing import Optional
from dukascopy_python.instruments import *
import dukascopy_python

class Session:
    def __init__(self, start:datetime.datetime, end:datetime.datetime, start_time:datetime.time, end_time:datetime.time, months:int,starting_balance:float,entry:float,instrument,strategy:str,candle_interval):
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
def setupSession()->Optional[Session]:
    while True:
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
            break

        except ValueError:
            print("Invalid Datetime Format")

    while True:     
        try:
            STARTING_BALANCE=float(input("Input starting balance: $"))
            ENTRY=float(input("Input entry amount per trade: $"))
            INSTRUMENT=INSTRUMENT_US_TECH_US_USD
            break

        except ValueError:
            print("Wrong Value")
        
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