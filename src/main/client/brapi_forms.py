from decimal import Decimal
from typing import List

from pydantic import BaseModel, model_validator


class AvailableAssets(BaseModel):
    assets: list[str]


class AssetPrice(BaseModel):
    date: int  # unix timestamp
    close: Decimal

    @model_validator(mode='after')
    def round_prices(self):
        self.close = round(self.close, 3)
        return self


class AssetPrices(BaseModel):
    prices: List[AssetPrice]

    def __getitem__(self, index):
        return self.prices[index]

    def __iter__(self):
        return iter(self.prices)

    def __len__(self):
        return len(self.prices)
