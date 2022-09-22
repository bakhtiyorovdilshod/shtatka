from sqlalchemy import select, func
from fastapi import Request

from core.settings import database


class Queryset:
    model = None

    @classmethod
    async def all_for_pagination(cls, page: int, page_size: int, request: Request = None):
        domain_name = request.url._url.split('?')[0]
        _page = cls.get_page(page)
        query = select([cls.model])
        query = query.limit(page_size).offset(_page * page_size)
        count = await cls.count()
        next_page = cls.get_next_page(page, page_size, count, domain_name=domain_name)
        prev_page = cls.get_prev_page(page, page_size, domain_name=domain_name)
        results = await database.fetch_all(query)
        return dict(next=next_page, previous=prev_page, count=count, results=results)

    @classmethod
    async def count(cls):
        query = select([func.count(cls.model.c.id).label('total_count')])
        result = await database.fetch_one(query)
        return result['total_count']

    @classmethod
    def get_page(cls, page: int):
        if page <= 0:
            page = 0
        else:
            page -= 1
        return page

    @classmethod
    def get_next_page(cls, page: int, page_size: int, count: int, domain_name: str):
        next_page = page + 1
        if (count / page_size) < next_page:
            return None
        return f"{domain_name}?page={next_page}&page_size={page_size}"

    @classmethod
    def get_prev_page(cls, page: int, page_size: int, domain_name: str):
        if page <= 1:
            return None
        return f"{domain_name}?page={page - 1}&page_size={page_size}"

    # @classmethod
    # def pagination_for_shtatka_list(cls, page: int, page_size: int, model,  request: Request):
    #     domain_name = request.url._url.split('?')[0]
    #     _page = cls.get_page(page)
    #     query = select([cls.model])
    #     if filter:
    #         filter_field = values['filter_field']
    #         query = query.where(
    #             cls.model.c.filter_field ==
    #         )
    #     query = query.limit(page_size).offset(_page * page_size)
    #     count = await cls.count()
    #     next_page = cls.get_next_page(page, page_size, count, domain_name=domain_name)
    #     prev_page = cls.get_prev_page(page, page_size, domain_name=domain_name)
    #     results = await database.fetch_all(query)
    #     return dict(next=next_page, previous=prev_page, count=count, results=results)