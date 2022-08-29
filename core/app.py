from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider

from api.user.endpoints.user import router as user_router
from fastapi.middleware.cors import CORSMiddleware
from core.settings import settings, database


app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
app.include_router(prefix='/api/v1', router=user_router)
app.mount('/admin', admin_app)


@app.on_event("startup")
async def startup():
    await admin_app.configure(template_folders=["templates"])
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

