from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, RootModel


class AvailableAssets(BaseModel):
    assets: list[str]


class AssetPrice(BaseModel):
    """
    {
        "date":1690462800,
        "open":30.850000381469727,
        "high":30.850000381469727,
        "low":30.75,
        "close":30.799999237060547,
        "volume":550900,
        "adjustedClose":null
    }
    """
    pass


class AssetPrices(BaseModel):
    prices: List[AssetPrice]

    def __getitem__(self, index):
        return self.prices[index]

    def __iter__(self):
        return iter(self.prices)

    def __len__(self):
        return len(self.prices)
