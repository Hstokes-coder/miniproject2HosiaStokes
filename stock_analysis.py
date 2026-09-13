# INF601 - Advanced Programming in Python
# Hosia Stokes
# Mini Project 2

"""
stock_analysis.py

Downloads the last 10 trading days of price data for 5 stock tickers
using yfinance, computes some basic statistics with NumPy, and saves
one chart per ticker into the charts/ folder using Matplotlib.
"""

import os

import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# The 5 tickers we're analyzing. Kept as a plain list at the top of
# the file so it's easy to see (and change) which stocks the script
# looks at without having to dig through the rest of the code.
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

# How many trading days of history to pull for each ticker.
NUM_DAYS = 10

# Folder where the generated charts get saved.
CHARTS_DIR = "charts"


def fetch_stock_data(ticker, num_days):
    """
    Download the most recent `num_days` of daily price data for one
    ticker using yfinance.

    yf.Ticker(ticker) creates a handle for that one stock, and
    .history(period="10d") asks Yahoo Finance for its last 10 days of
    data. yfinance automatically skips weekends and market holidays,
    so this gives us 10 actual trading days, not 10 calendar days.

    Returns a pandas DataFrame: one row per trading day, with columns
    like "Open", "High", "Low", "Close", and "Volume".
    """
    stock = yf.Ticker(ticker)
    history = stock.history(period=f"{num_days}d")
    return history


def analyze_stock(history):
    """
    Given one ticker's price history (as returned by fetch_stock_data),
    compute some basic statistics using NumPy.

    history: a pandas DataFrame with a "Close" column.

    Returns a dictionary of stats:
      - "closes":           the closing prices as a NumPy array
      - "average_close":    the mean closing price over the period
      - "min_close":        the lowest closing price
      - "max_close":        the highest closing price
      - "daily_pct_change": day-over-day percent change, as a NumPy array
      - "volatility":       how much the daily percent change bounced
                             around (its standard deviation)
    """
    # .to_numpy() converts the pandas "Close" column into a plain
    # NumPy array, which is what the calculations below run on.
    closes = history["Close"].to_numpy()

    average_close = np.mean(closes)
    min_close = np.min(closes)
    max_close = np.max(closes)

    # np.diff(closes) gives the day-over-day change in price (today's
    # close minus yesterday's close) for every day except the first
    # one. Dividing that by closes[:-1] (every close except the very
    # last day) and multiplying by 100 turns it into a percentage -
    # how much the price moved, relative to the previous day's price.
    daily_pct_change = (np.diff(closes) / closes[:-1]) * 100

    # Standard deviation measures how spread out the daily percent
    # changes are. A bigger number means the price swung around more
    # from day to day (more volatile); a smaller number means the
    # price was more stable across the 10 days.
    volatility = np.std(daily_pct_change)

    return {
        "closes": closes,
        "average_close": average_close,
        "min_close": min_close,
        "max_close": max_close,
        "daily_pct_change": daily_pct_change,
        "volatility": volatility,
    }


def plot_stock(ticker, history, charts_dir):
    """
    Create a line chart of one ticker's closing price over the 10
    trading days and save it as a PNG inside charts_dir.

    history: the price DataFrame for this ticker (from
             fetch_stock_data). Its row labels (history.index) are
             the actual trading dates, and "Close" is the column of
             closing prices.
    charts_dir: the folder to save the PNG into (created by main()
                before this function is ever called).

    Returns the path of the PNG file that was saved.
    """
    # history.index is a DatetimeIndex - the trading dates. Formatting
    # each one as "MM-DD" keeps the x-axis labels short and readable
    # instead of printing a full timestamp under every point.
    dates = history.index.strftime("%m-%d")
    closes = history["Close"].to_numpy()

    plt.figure(figsize=(8, 5))
    plt.plot(dates, closes, marker="o")

    plt.title(f"{ticker} Closing Price - Last {len(closes)} Trading Days")
    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)")
    plt.grid(True)
    plt.tight_layout()

    chart_path = os.path.join(charts_dir, f"{ticker}_closing_price.png")
    plt.savefig(chart_path)

    # Close the figure once it's saved. Without this, matplotlib
    # keeps every figure open in memory - fine for 5 tickers, but a
    # bad habit that adds up if this script grows to analyze more.
    plt.close()

    return chart_path


def main():
    # exist_ok=True: this is fine to call even if charts/ already
    # exists from a previous run.
    os.makedirs(CHARTS_DIR, exist_ok=True)

    # Holds every ticker's price history and stats, keyed by ticker
    # symbol, in case you want to inspect them after main() returns.
    results = {}

    for ticker in TICKERS:
        print(f"Fetching {NUM_DAYS} days of data for {ticker}...")
        history = fetch_stock_data(ticker, NUM_DAYS)
        stats = analyze_stock(history)
        results[ticker] = {"history": history, "stats": stats}

        print(f"  Average close: ${stats['average_close']:.2f}")
        print(f"  Min close:     ${stats['min_close']:.2f}")
        print(f"  Max close:     ${stats['max_close']:.2f}")
        print(f"  Volatility:    {stats['volatility']:.2f}%")

        chart_path = plot_stock(ticker, history, CHARTS_DIR)
        print(f"  Saved chart: {chart_path}")

    return results


if __name__ == "__main__":
    main()
