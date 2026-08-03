from classes.Session import setupSession
from functions.fetch_data import fetchInstrumentData
from functions.backtest_run import runBacktest
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
