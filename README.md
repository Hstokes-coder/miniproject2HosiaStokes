# Stock Analysis - Mini Project 2

A beginner-friendly Python program that downloads recent stock price
data, runs some basic statistics on it, and produces a chart for each
stock analyzed.

## What It Does

`stock_analysis.py` downloads the last **10 trading days** of price
data for **5 stock tickers**, calculates a handful of basic
statistics for each one with NumPy, and saves a closing-price chart
for each ticker as a PNG using Matplotlib.

**Tickers analyzed:**

- AAPL (Apple)
- MSFT (Microsoft)
- GOOGL (Alphabet/Google)
- AMZN (Amazon)
- TSLA (Tesla)

## Data Source

Price data comes from yfinance, a Python library that retrieves
historical stock data from Yahoo Finance. The program requests the
most recent 10 days of available historical data for each ticker.
The returned rows use actual market trading dates.

## How It Works

### 1. Fetching the data

For each of the 5 tickers, the program uses yfinance to download a
table of daily price data (open, high, low, close, and volume) for
the last 10 trading days.

### 2. NumPy calculations

For each ticker, the program uses NumPy to calculate:

- **Average close** - the mean closing price across the 10 days.
- **Minimum close** - the lowest closing price in that period.
- **Maximum close** - the highest closing price in that period.
- **Daily percent change** - how much the price moved from one day to
  the next, as a percentage (for example, going from $100 to $102 is
  a +2% change).
- **Volatility** - the standard deviation of those daily percent
  changes. A higher number means the price swung around more from day
  to day; a lower number means it stayed more stable.

### 3. Charts

Using Matplotlib, the program creates one line chart per ticker
showing its closing price across the 10 trading days, with a clear
title and labeled axes. Each chart is saved as a PNG file inside the
`charts/` folder (which the program creates automatically if it
doesn't already exist), for example `charts/AAPL_closing_price.png`.

## Setup

### 1. Create and activate a virtual environment

From inside the project folder:

```
python3 -m venv .venv
source .venv/bin/activate
```

(On Windows, activate it with `.venv\Scripts\activate` instead.)

You'll know it worked because your terminal prompt will show `(.venv)`
at the start of the line.

### 2. Install the required packages

With the virtual environment activated, install everything listed in
`requirements.txt`:

```
pip install -r requirements.txt
```

### 3. Run the program

```
python stock_analysis.py
```

The program will print each ticker's stats to the terminal as it
runs, and save all 5 charts into the `charts/` folder.

## Output

- **Terminal output** - for each ticker, the average, minimum, and
  maximum closing price, plus its volatility.
- **`charts/`** - one PNG chart per ticker, showing that ticker's
  closing price over the 10 trading days. This folder is created
  automatically the first time you run the program.

## AI Usage

I used Claude Code (via Claude's Cowork mode) as a coding assistant
while building this project. It helped draft and explain portions of
`stock_analysis.py` - including the yfinance data-fetching function,
the NumPy statistics, and the Matplotlib charting code - one section
at a time, with an explanation of what each part does before moving
on to the next. I ran the program and reviewed the generated output
and charts myself.
