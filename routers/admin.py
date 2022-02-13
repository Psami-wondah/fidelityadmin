from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Form, Depends, UploadFile, status
from auth.oauth2 import get_current_admin, verify_password, get_password_hash
from schemas import admin_schemas, generic_schemas
from utils.cloudinary import upload_image
from fastapi.responses import JSONResponse
from db.config import db
from pymongo.errors import DuplicateKeyError
from pydantic import BaseModel

app = APIRouter(
    tags=["Admin Profile 👔"],
)


class ChangePassword(BaseModel):
    current_password: str
    new_password: str

@app.get("/admin/profile", response_model=admin_schemas.AdminUpdate)
async def get_admin_profile(admin: admin_schemas.Admin = Depends(get_current_admin)):
    return admin

@app.put("/admin/profile", response_model=admin_schemas.AdminUpdate)
async def update_admin_profile(
    image: Optional[UploadFile] = None,
    username: Optional[str] = Form(None),
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    admin: admin_schemas.Admin = Depends(get_current_admin),
):
    if image:
        image_data = image.content_type.split("/")
        if image_data[0] != "image":
            return JSONResponse({"message": "file is not an image"})
        image_url = await upload_image(image=image.file)
    else:
        image_url = None
    if username == admin.username:
        username = None
    admin_update_data = admin_schemas.AdminUpdate(
        username=username,
        first_name=first_name,
        last_name=last_name,
        profile_image_url=image_url,
        last_updated_at=datetime.utcnow(),
    )
    data = admin_update_data.dict()
    cleaned_data = data.copy()
    for datum in data:
        if data[datum] == None:
            del cleaned_data[datum]
    try:
        db.admins.find_one_and_update(
            {"username": admin.username}, {"$set": cleaned_data}
        )
    except DuplicateKeyError:
        return JSONResponse(
            {"message": "username already exists"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if username:
        admin.username = username
    admin_from_db = db.admins.find_one({"username": admin.username})

    return admin_schemas.AdminUpdate(**admin_from_db)


@app.put(
    "/admin/profile/change-password", response_model=generic_schemas.ResponseMessage
)
async def change_password(
    passwords: ChangePassword, admin: admin_schemas.Admin = Depends(get_current_admin)
):
    password_status = verify_password(passwords.current_password, admin.hashed_password)
    if password_status:
        db.admins.find_one_and_update(
            {"username": admin.username},
            {"$set": {"hashed_password": get_password_hash(passwords.new_password)}},
        )
        return {"message": "password change successful"}
    return JSONResponse(
        {"message": "incorrect current password"},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
