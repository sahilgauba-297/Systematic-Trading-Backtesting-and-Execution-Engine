import numpy as np
import pandas as pd

from signals import SignalEngine
from positions import PositionEngine
from backtest import BacktestEngine


class WalkForwardTest:

    def __init__(self,
                 train_size=100,
                 test_size=50):

        self.train_size = train_size
        self.test_size = test_size

    def run(self, df):

        df = df.copy().reset_index(drop=True)

        results = []

        start = 0
        n = len(df)

        while start + self.train_size + self.test_size < n:

            train_end = start + self.train_size
            test_end = train_end + self.test_size

            test_df = df.iloc[train_end:test_end].copy()

            signal_engine = SignalEngine()
            position_engine = PositionEngine()
            backtest_engine = BacktestEngine()

            test_df = signal_engine.generate_signals(test_df)
            test_df = position_engine.generate_positions(test_df)

            test_df = backtest_engine.run_backtest(test_df)
            metrics = backtest_engine.performance_metrics(test_df)

            metrics["window_start"] = train_end
            metrics["window_end"] = test_end

            results.append(metrics)

            start += self.test_size

        return pd.DataFrame(results)