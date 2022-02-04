from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Form
from schemas import admin_schemas, token_schemas
from pymongo.errors import DuplicateKeyError
from pydantic import BaseModel
from typing import Any
from auth.oauth2 import (
    get_password_hash,
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
)
from db.config import db
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm


app = APIRouter(
    tags=["Auth 🔐"],
)


class RegRes(BaseModel):
    message: str
    admin: admin_schemas.AdminBase


class AdminLogin(BaseModel):
    username: str
    password: str

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.username = self.username.lower()


@app.post("/token", response_model=token_schemas.Token)
async def login_for_access_token(data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, data.username, data.password)
    if not user:
        return JSONResponse(
            {"message": "Incorrect username or password"},
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.is_superuser == False:
        return JSONResponse(
            {"message": "Sorry you don't have access"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires": f"{ACCESS_TOKEN_EXPIRE_MINUTES}",
    }


@app.post(
    "/admin/auth/create", status_code=status.HTTP_201_CREATED, response_model=RegRes
)
async def create_admin(admin: admin_schemas.AdminCreate):
    admin_data = admin_schemas.Admin(
        username=admin.username,
        first_name=admin.first_name,
        last_name=admin.last_name,
        hashed_password=get_password_hash(admin.password),
        is_superuser=False,
        created_at=datetime.utcnow(),
        last_updated_at=datetime.utcnow(),
    )
    try:
        db.admins.insert_one(admin_data.dict())
    except DuplicateKeyError:
        return JSONResponse(
            {"message": "username already exists"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    admin_from_db = db.admins.find_one({"username": admin.username})
    return {
        "message": "Admin Created Successfully",
        "admin": admin_schemas.AdminBase(**admin_from_db),
    }


@app.post("/admin/auth/login", response_model=token_schemas.Token)
async def login(data: AdminLogin):
    admin = authenticate_user(db=db, username=data.username, password=data.password)
    if not admin:
        return JSONResponse(
            {"message": "Incorrect username or password"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    if admin.is_superuser == False:
        return JSONResponse(
            {"message": "Sorry you don't have access"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires": f"{ACCESS_TOKEN_EXPIRE_MINUTES}",
    }



