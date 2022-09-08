from fastapi import FastAPI

from api.user.endpoints.user import router as user_router
from api.department.endpoints.department import router as department_router
from api.department.endpoints.settings import router as settings_router
from fastapi.middleware.cors import CORSMiddleware
from core.settings import settings, database

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
app.include_router(prefix='/api/v1', router=user_router)
app.include_router(prefix='/api/v1/shtat', router=department_router)
app.include_router(prefix='/api/v1/shtat/department/settings', router=settings_router)


@app.on_event("startup")
async def startup():
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

