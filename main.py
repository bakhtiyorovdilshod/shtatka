import uvicorn
from fastapi.security import OAuth2PasswordBearer

from core.app import app

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token/")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
