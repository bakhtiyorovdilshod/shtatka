from fastapi import APIRouter, Request, Depends

from api.client.schemas.document import AcceptDocumentSchema
from api.client.services.document import DocumentService
from api.user.schemas.user import UserDetailSchema
from api.user.services.auth import UserAuthenticationService, is_authenticated


router = APIRouter()


@router.post('/send/',  tags=['documents'])
async def create_department(data: AcceptDocumentSchema):
    result = await DocumentService().accept_client_documents(data=data)
    return result