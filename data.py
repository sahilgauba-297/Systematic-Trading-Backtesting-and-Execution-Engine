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