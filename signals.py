import numpy as np
import pandas as pd


class SignalEngine:

    def __init__(self,
                 momentum_window=10,
                 short_window=5,
                 long_window=20,
                 vol_window=20):

        self.momentum_window = momentum_window
        self.short_window = short_window
        self.long_window = long_window
        self.vol_window = vol_window

    def generate_signals(self, df):

        df = df.copy()

        # Multi window momentum
        df["momentum_short"] = df["Close_SPY"].pct_change(self.short_window)
        df["momentum_long"] = df["Close_SPY"].pct_change(self.long_window)

        df["momentum"] = (
            0.5 * df["momentum_short"] +
            0.5 * df["momentum_long"]
        )

        # smoothing
        df["momentum"] = df["momentum"].rolling(3).mean()

        # volatility
        df["volatility"] = df["returns"].rolling(5).std()

        vol_mean = df["volatility"].rolling(self.vol_window).mean()
        vol_std = df["volatility"].rolling(self.vol_window).std()

        # dynamic threshold
        df["vol_filter"] = df["volatility"] < (vol_mean + 0.5 * vol_std)

       
        df["signal"] = np.where(
            (df["momentum"] > 0.002) & (df["vol_filter"]),
            1,
            np.where(
                (df["momentum"] < -0.002) & (df["vol_filter"]),
                -1,
                0
            )
        )


        df["signal"] = df["signal"].fillna(0)

        return df