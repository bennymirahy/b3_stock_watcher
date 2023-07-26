from pydantic import BaseModel


class PaginatorForm(BaseModel):
    page: int = None
    rows_per_page: int = None
    sort_by: str = None
    descending: bool = None
