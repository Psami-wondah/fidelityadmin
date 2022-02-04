from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends
from schemas import user_schemas, admin_schemas, wallet_schemas
from auth.oauth2 import get_current_admin
from db.config import db
from serializers.user_serializers import user_serialize_list, user_serialize_dict
from fastapi_pagination import Page, add_pagination, paginate
from bson.objectid import ObjectId

from serializers.wallet_serializers import wallet_serialize_dict

app = APIRouter(tags=["Users 👤"])


@app.get("/admin/users", response_model=Page[user_schemas.UserBase])
async def get_all_users(admin: admin_schemas.Admin = Depends(get_current_admin)):
    users_from_db = db.users.find()
    users = user_serialize_list(users_from_db)
    return paginate(users)


@app.get("/admin/users/plan", response_model=Page[user_schemas.UserBase])
async def get_all_users_with_a_plan(
    admin: admin_schemas.Admin = Depends(get_current_admin),
):
    users_from_db = db.users.find(
        {
            "$or": [
                {"plans": {"$size": 1}},
                {"plans": {"$size": 2}},
                {"plans": {"$size": 3}},
                {"plans": {"$size": 4}},
            ]
        }
    )
    users = user_serialize_list(users_from_db)
    return paginate(users)


@app.get("/admin/user/{uin}", response_model=user_schemas.User)
async def get_user(uin: str, admin: admin_schemas.Admin = Depends(get_current_admin)):
    user = db.users.find_one({"uin": uin})
    return user_serialize_dict(user)


@app.get("/admin/user/{uin}/wallet", response_model=wallet_schemas.Wallet)
async def get_user_wallet(
    uin: str, admin: admin_schemas.Admin = Depends(get_current_admin)
):
    user = db.users.find_one({"uin": uin})
    wallet = db.wallets.find_one({"_id": user["wallet"]})
    return wallet_serialize_dict(wallet)


@app.put("/admin/user/{uin}/wallet", response_model=wallet_schemas.Wallet)
async def update_user_wallet(
    wallet: wallet_schemas.WalletUpdate,
    uin: str,
    admin: admin_schemas.Admin = Depends(get_current_admin),
):
    user = db.users.find_one({"uin": uin})
    wallet = wallet.dict()
    cleaned_wallet = wallet.copy()
    for item in wallet:
        if wallet[item] == None:
            del cleaned_wallet[item]
    cleaned_wallet["updatedAt"] = datetime.utcnow()

    db.wallets.find_one_and_update({"_id": user["wallet"]}, {"$set": cleaned_wallet})
    updated_wallet = db.wallets.find_one({"_id": user["wallet"]})
    return updated_wallet


add_pagination(app)
