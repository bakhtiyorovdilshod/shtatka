from core.settings import database


class Queryset:
    model = None

    @classmethod
    async def all_for_pagination(cls, page: int, page_size: int):
        _page = cls.get_page(page)
        query = await cls.base_query()
        query = query.order_by(cls.model.c.id.desc())
        query = query.limit(page_size).offset(_page * page_size)
        count = await cls.count()
        next_page = cls.get_next_page(page, page_size, count)
        prev_page = cls.get_prev_page(page, page_size)
        results = await database.fetch_all(query)
        return dict(next=next_page, previous=prev_page, count=count, results=results)


    @classmethod
    def get_page(cls, page: int):
        if page <= 0:
            page = 0
        else:
            page -= 1
        return page

    @classmethod
    def get_next_page(cls, page: int, page_size: int, count: int):
        next_page = page + 1
        if (count / page_size) < next_page:
            return None
        return f"page={next_page}&page_size={page_size}"

    @classmethod
    def get_prev_page(cls, page: int, page_size: int):
        if page <= 1:
            return None
        return f"page={page - 1}&page_size={page_size}"