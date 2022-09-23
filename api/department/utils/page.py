from sqlalchemy import select, func

from core.settings import database


async def get_count(main_model):
    query = select([func.count(main_model.c.id).label('total_count')])
    result = await database.fetch_one(query)
    return result['total_count']


def get_page(page: int):
    if page <= 0:
        page = 0
    else:
        page -= 1
    return page


def get_next_page(page: int, page_size: int, count: int, domain_name: str):
    next_page = page + 1
    if (count / page_size) < next_page:
        return None
    return f"{domain_name}?page={next_page}&page_size={page_size}"


def get_prev_page(page: int, page_size: int, domain_name: str):
    if page <= 1:
        return None
    return f"{domain_name}?page={page - 1}&page_size={page_size}"