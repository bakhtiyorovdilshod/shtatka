from fastapi import APIRouter
from typing import  Optional
from api.user.services.user import UserService

router = APIRouter()


@router.get('/shtat/select_user/',  tags=['user'])
async def search_user(search: Optional[str] = None):
    return await UserService().search_user(name=search)