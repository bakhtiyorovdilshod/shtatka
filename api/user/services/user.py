from typing import Union, Optional
import requests


class UserService:
    @staticmethod
    async def search_user(name: Optional[str] = None):
        headers = {
            'content-type': 'application/json; charset=utf8'
        }
        url = f'https://hr.mf.uz/api/v1/shtat/select_user/?search={name}'
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return response.json()
        return []

