import pandas as pd
import numpy as np
import yfinance as yf
import datetime
from signals import SignalEngine
from positions import PositionEngine
from backtest import BacktestEngine
from walk_forward import WalkForwardTest

class MarketDataEngine:

    def __init__(self, ticker="SPY", start="2025-01-01", end=None):
        self.ticker = ticker
        self.start = start
        self.end = end or datetime.date.today().strftime("%Y-%m-%d")

    def load_data(self):

        df = yf.download(
            self.ticker,
            start=self.start,
            end=self.end,
            progress=False
        )

        df.reset_index(inplace=True)

        # flatten MultiIndex columns 
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [
                col[0] if col[1] == "" else f"{col[0]}_{col[1]}"
                for col in df.columns
            ]

        return df

    # features
    def add_features(self, df):

        df["returns"] = df["Close_SPY"].pct_change()
        df["volatility"] = df["returns"].rolling(window=5).std()
        df["volume_avg"] = df["Volume_SPY"].rolling(window=5).mean()
        df["spread_proxy"] = (df["High_SPY"] - df["Low_SPY"]) / df["Close_SPY"]

        return df

    # pipeline
    def process(self):

        df = self.load_data()
        df = self.add_features(df)

        return df

def run_pipeline(df):

    signal_engine = SignalEngine(
        momentum_window=5,
        vol_window=20
    )
    df = signal_engine.generate_signals(df)

    position_engine = PositionEngine()
    df = position_engine.generate_positions(df)

    backtest = BacktestEngine(
    initial_capital=1.0,
    base_slippage_bps=1,
    base_spread_bps=2
)

    df = backtest.run_backtest(df)
    metrics = backtest.performance_metrics(df)

    return df, metrics



if __name__ == "__main__":

    engine = MarketDataEngine(
        ticker="SPY",
        start="2025-01-01"
    )

    df = engine.process()

    df, metrics = run_pipeline(df)

    print("\nPerformance")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    print("\nFinal Equity Curve")
    print(df[["Date", "equity_curve"]].tail(10))

    print("\nData Summary")
    print(df.head())

    print("\nColumns")
    print(df.columns)

    print("\nShape")
    print(df.shape)





import matplotlib.pyplot as plt

def plot_equity(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df["Date"], df["equity_curve"])
    plt.title("Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Equity")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

plot_equity(df)

def plot_drawdown(df):
    equity = df["equity_curve"]
    peak = equity.cummax()
    drawdown = (equity - peak) / peak

    plt.figure(figsize=(10, 4))
    plt.plot(df["Date"], drawdown)
    plt.title("Drawdown Curve")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

plot_drawdown(df)


def plot_positions(df):
    plt.figure(figsize=(10, 5))

    plt.plot(df["Date"], df["Close_SPY"], label="Price")
    plt.scatter(df["Date"], df["Close_SPY"],
                c=df["position"], cmap="coolwarm", alpha=0.5)

    plt.title("Price with Position Overlay")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("PricePosition.png", dpi=300)
    plt.show()
plot_positions(df)