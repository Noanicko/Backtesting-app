# Finance Market Backtesting App

A Python-based backtesting framework for evaluating intraday trading strategies using historical market data from Dukascopy.

## Features

* Historical market data retrieval using `dukascopy-python`
* Opening Range Breakout (ORB) strategy implementation
* Multi-timeframe analysis (5-minute and 1-hour candles)
* Technical indicators:

  * RSI
  * EMA 
  * VWAP
* Configurable trading session
* Trade management with:

  * Take Profit
  * Stop Loss
  * Time-based exits
  * Break-even exits
* Performance statistics including:

  * Win rate
  * Profit factor
  * Net profit
  * Maximum drawdown
* Account balance growth visualization

## Project Structure

```text
backtesting-app/
│
├── main.py
├── classes/
│   ├── Session.py
│   ├── Backtest.py
│   ├── Trade.py
│   ├── Candle.py
│   └── InstrumentData.py
│
├── functions/
│   ├── session.py
│   ├── data_fetcher.py
│   ├── indicators.py
│   ├── trade_logger.py
│   └── backtest_run.py
│
├── strategies/
│   └── orb.py
│
└── README.md
```

## Requirements

* Python 3.11+
* pandas
* matplotlib
* pandas-ta
* dukascopy-python

Install dependencies:

```bash
pip install pandas matplotlib pandas-ta dukascopy-python
```

## Running

Start the application with:

```bash
python main.py
```

The program will prompt you for:

* Backtest start date
* Backtest end date
* Session start time
* Session end time
* Starting account balance
* Position size per trade

## Strategy

The current implementation uses an **Opening Range Breakout (ORB)** strategy.

Trade entries are evaluated using:

* Opening range breakout
* 1-hour EMA trend confirmation
* VWAP position
* RSI confirmation

Trades are automatically managed using predefined Take Profit, Stop Loss, break-even logic, and maximum holding time.

## Output

After each backtest, the application provides:

* Total trades
* Win/loss statistics
* Win rate
* Profit factor
* Net profit
* Maximum drawdown
* Balance growth chart

## Future Improvements

* Additional trading strategies
* Multiple instruments
* Configurable risk management
* Commission and spread simulation
* Strategy optimization
* Parameter sweeps
* Export trades to CSV
* Interactive charts

## Disclaimer

This project is intended for educational and research purposes only.

