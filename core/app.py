from fastapi import FastAPI

from api.user.endpoints.user import router as user_router
from api.department.endpoints.department import router as department_router
from api.department.endpoints.settings import router as settings_router
from api.client.endpoints.document import router as document_router
from api.department.endpoints.shtatka import router as department_shtatka_router
from fastapi.middleware.cors import CORSMiddleware
from core.settings import settings, database
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(prefix='/api/v1', router=user_router)
app.include_router(prefix='/api/v1/shtat', router=department_router)
app.include_router(prefix='/api/v1/shtat/department/settings', router=settings_router)
app.include_router(prefix='/api/v1/shtat/document', router=document_router)
app.include_router(prefix='/api/v1/shtat/department/shtatka_document', router=department_shtatka_router)


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

