import pandas as pd
from odin.utilities.mixins.strategy_mixins import (
    LongStrategyMixin,
    EqualBuyProportionMixin, 
    TotalSellProportionMixin
)


class MovingAverageCrossoverStrategy(
    LongStrategyMixin, EqualBuyProportionMixin, 
    TotalSellProportionMixin
):
    def buy_indicator(self, feats):
        """Implementation of abstract base class method."""
        return (
            feats.name == "AAPL" and
            feats["short_mavg"] > feats["long_mavg"]
        )

    def sell_indicator(self, feats):
        """Implementation of abstract base class method."""
        return False

    def exit_indicator(self, feats):
        """Implementation of abstract base class method."""
        return (
            feats["long_mavg"] > feats["short_mavg"]
        )

    def generate_features(self):
        """Implementation of abstract base class method."""
        long_bars = self.portfolio.data_handler.bars.ix[:, -200:, :]
        short_bars = self.portfolio.data_handler.bars.ix[:, -50:, :]
        feats = pd.DataFrame(index=short_bars.minor_axis)
        feats["long_mavg"] = long_bars["adj_price_close"].mean()
        feats["short_mavg"] = short_bars["adj_price_close"].mean()
        return feats

    def generate_priority(self, feats):
        """Implementation of abstract base class method."""
        return self.portfolio.data_handler.bars.ix[
            "adj_price_open", -1, :
        ].dropna().index
