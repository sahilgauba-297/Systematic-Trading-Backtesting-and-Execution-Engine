import pandas as pd
import numpy as np


class PositionEngine:

    def __init__(self, max_position=1):
        self.max_position = max_position

    def generate_positions(self, df):

        df = df.copy()
        
        df["position"] = df["signal"].shift(1)

        df["position"] = df["position"].clip(-self.max_position, self.max_position)

        df["position"] = df["position"].fillna(0)

        return df