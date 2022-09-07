from fastapi import Depends, HTTPException, status, Query, WebSocket
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from api.user.schemas.user import UserDetailSchema
from core.settings import settings, database
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/token/", auto_error=True)
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/doc/login/")


class UserAuthenticationService:
    def create_access_token(self, user_id):
        expire = datetime.now() + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAY)
        print(expire)
        to_encode = dict(exp=expire, user_id=user_id)
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        # try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={'verify_signature': False})
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        # except JWTError:
        #     raise credentials_exception
        user = await database.fetch_one(query='SELECT id, full_name, username, role_id, is_active FROM users WHERE id = :id', values={'id': user_id})
        if not user:
            raise credentials_exception
        return user


async def is_authenticated(user: UserDetailSchema = Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
