from sqlalchemy.orm import Query

__all__ = [
    "Paginator",
]

from app.core.response import ListDataSchema


class Paginator:
    def __init__(self, query: Query, page_size: int):
        self.query = query
        self.total = query.count()
        self.page_size = page_size

    def total_pages(self) -> int:
        return (self.total + self.page_size - 1) // self.page_size

    def get_page_query(self, page) -> Query:
        offset = (page - 1) * self.page_size
        limit = self.page_size
        return self.query.offset(offset).limit(limit)

    def page(self, page) -> ListDataSchema:
        offset = (page - 1) * self.page_size
        limit = self.page_size
        results = self.query.offset(offset).limit(limit).all()
        return ListDataSchema(list=results, total=self.total)
