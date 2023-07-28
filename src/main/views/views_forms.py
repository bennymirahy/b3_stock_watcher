from pydantic import BaseModel, Field


class PaginatorForm(BaseModel):
    page: int
    sort_by: str = Field(alias='sortBy')
    rows_per_page: int = Field(alias='rowsPerPage')
    descending: bool
