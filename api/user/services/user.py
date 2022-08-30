from typing import Union, Optional
import requests, json

from api.user.schemas.user import UpdateOrganizationSchema
from api.user.utils.page import fix_pagination


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

    @staticmethod
    async def get_organizations(page: int, page_size: int, domain_name: str):
        headers = {
            'content-type': 'application/json; charset=utf8'
        }
        url = f'https://hr.mf.uz/api/v1/shtat/organization/?page={page}&page_size={page_size}'
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return fix_pagination(data=response.json(), domain_name=domain_name)
        return []

    @staticmethod
    async def get_detail_organization(organization_id: int):
        headers = {
            'content-type': 'application/json; charset=utf8'
        }
        url = f'https://hr.mf.uz/api/v1/shtat/organization/{organization_id}/'
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return response.json()
        return []

    @staticmethod
    async def edit_organization(organization_id: int, data=UpdateOrganizationSchema):
        headers = {
            'content-type': 'application/json; charset=utf8'
        }
        url = f'https://hr.mf.uz/api/v1/shtat/organization/{organization_id}/'
        json_data = {
            'chapter_code': data.chapter_code,
            'department_code': data.department_code,
            'small_department_code': data.small_department_code
        }
        json_data = json.dumps(json_data)
        response = requests.put(url=url, headers=headers, data=json_data, verify=False)
        return response.status_code

