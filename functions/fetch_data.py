from classes.Session import Session
from typing import Optional
from classes.InstrumentData import InstrumentData
import dukascopy_python

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