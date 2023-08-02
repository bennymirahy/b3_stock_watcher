from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class PaginatorForm(BaseModel):
    page: int
    sort_by: Optional[str]= None
    rows_per_page: int = Field(alias='itemsPerPage')

    @model_validator(mode='before')
    def parse_order_by(self):
        if not self['sortBy']:
            return self
        desc = self.pop('sortDesc')
        sort = self.pop('sortBy')[0]
        self['sort_by'] = sort
        if desc:
            self['sort_by'] = '-' + sort
        return self


class AssetForm(BaseModel):
    ref_price: Decimal
    lower_limit: int
    upper_limit: int
    interval: int

    @model_validator(mode='after')
    def check_price_tunel_ranges(self):
        if not (-100 <= self.lower_limit <= 0):
            raise ValueError('O limite inferior do túnel deve estar entre -100% e 0%')
        if not self.upper_limit >= 0:
            raise ValueError('O limite superior do túnel deve ser positivo')
        return self
