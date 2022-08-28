from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.settings import settings, database


app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
# app.include_router(prefix='/api/v1/user', router=user_router)


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

