import numpy as np
import pandas as pd


class BacktestEngine:

    def __init__(self,
                 initial_capital=1.0,
                 base_slippage_bps=1,
                 base_spread_bps=2):

        self.initial_capital = initial_capital
        self.base_slip = base_slippage_bps / 10000
        self.base_spread = base_spread_bps / 10000

    def run_backtest(self, df):

        df = df.copy().reset_index(drop=True)

        
        #Shifting position (execution delay)
        # signal today executes tomorrow
        # -----------------------------
        df["executed_position"] = df["position"].shift(1).fillna(0)


        # Position changes
        df["position_change"] = df["executed_position"].diff().abs().fillna(0)

        # 3. Volatility-adjusted slippage
       
        vol = df["returns"].rolling(10).std()
        vol = vol.fillna(vol.mean())

        df["dynamic_slippage"] = self.base_slip * (1 + vol * 50)

        # Spread cost
        spread = (df["High_SPY"] - df["Low_SPY"]) / df["Close_SPY"]
        df["spread_cost"] = spread * self.base_spread

        # total execution cost
        df["execution_cost"] = df["position_change"] * (
            df["dynamic_slippage"] + df["spread_cost"]
        )

        # strategy returns with fills
        df["gross_returns"] = df["executed_position"] * df["returns"]

        df["net_returns"] = df["gross_returns"] - df["execution_cost"]

        df["equity_curve"] = (1 + df["net_returns"]).cumprod()
        df["equity_curve"] *= self.initial_capital

        return df

    def performance_metrics(self, df):

        r = df["net_returns"].dropna()

        total_return = df["equity_curve"].iloc[-1] - self.initial_capital

        sharpe = (r.mean() / r.std()) * np.sqrt(252) if r.std() != 0 else 0

        peak = df["equity_curve"].cummax()
        drawdown = (df["equity_curve"] - peak) / peak
        max_drawdown = drawdown.min()

        turnover = df["position_change"].sum()

        return {
            "total_return_net": total_return,
            "sharpe_net": sharpe,
            "max_drawdown_net": max_drawdown,
            "turnover": turnover
        }