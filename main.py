from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas.admin_schemas import Admin
from routers.auth import app as auth_app
from routers.users import app as user_app
from routers.admin import app as admin_app
from fastapi_utils.tasks import repeat_every
# from backgroudtasks.send_email import send_new_user_email
from fastapi import BackgroundTasks

app = FastAPI(
    title="FidelityTrades",
    description="Admin Dashboard Apis",
    version="1",
)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_app)
app.include_router(admin_app)
app.include_router(user_app)


@app.on_event("startup")
async def startup():
    Admin.init()

# @app.on_event("startup")
# @repeat_every(seconds=60*5)
# async def send_email() -> None:
#     await send_new_user_email()
    
