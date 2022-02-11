from datetime import datetime
from fastapi import APIRouter, Depends, status
from schemas import user_schemas, admin_schemas, wallet_schemas, generic_schemas
from auth.oauth2 import get_current_admin
from db.config import db
from serializers.user_serializers import user_serialize_list, user_serialize_dict
from fastapi_pagination import Page, add_pagination, paginate
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse

from serializers.wallet_serializers import wallet_serialize_dict

app = APIRouter(tags=["Users 👤"])


@app.get("/admin/users", response_model=Page[user_schemas.UserBase])
async def get_all_users(search: str = None, admin: admin_schemas.Admin = Depends(get_current_admin)):
    if search==None:
        users_from_db = db.users.find()
    elif search:
        search = search.rstrip()
        if search == "":
            users_from_db = db.users.find()
        else:
            users_from_db = db.users.find({
                "$or": [
                    {"username": {
                        "$regex": f"^{search}",
                        "$options": "i"
                    }},
                    {"email": {
                        "$regex": f"^{search}",
                        "$options": "i"
                    }}
                ]
            })

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


@app.get("/admin/user/{uin}", response_model=user_schemas.UserDetails)
async def get_user_details(uin: str, admin: admin_schemas.Admin = Depends(get_current_admin)):
    user = db.users.find_one({"uin": uin})
    if user:
        wallet = db.wallets.find_one({"_id": user["wallet"]})
        user_dict = user_serialize_dict(user)
        wallet_dict = wallet_serialize_dict(wallet)
        return {
            "user": user_dict,
            "wallet": wallet_dict
        }
    return JSONResponse(
        {"message": "No user with that uin"}, status_code=status.HTTP_404_NOT_FOUND
    )





@app.put("/admin/user/{uin}/wallet", response_model=wallet_schemas.Wallet)
async def update_user_wallet(
    wallet: wallet_schemas.WalletUpdate,
    uin: str,
    admin: admin_schemas.Admin = Depends(get_current_admin),
):
    user = db.users.find_one({"uin": uin})
    if user:
        wallet = wallet.dict()
        cleaned_wallet = wallet.copy()
        for item in wallet:
            if wallet[item] == None:
                del cleaned_wallet[item]
        cleaned_wallet["updatedAt"] = datetime.utcnow()

        db.wallets.find_one_and_update(
            {"_id": user["wallet"]}, {"$set": cleaned_wallet}
        )
        updated_wallet = db.wallets.find_one({"_id": user["wallet"]})
        return updated_wallet
    return JSONResponse(
        {"message": "No user with that uin"}, status_code=status.HTTP_404_NOT_FOUND
    )


@app.put("/admin/user/{uin}/activate", response_model=generic_schemas.ResponseMessage)
async def deactivate_user(
    uin: str, admin: admin_schemas.Admin = Depends(get_current_admin)
):
    user = db.users.find_one({"uin": uin})
    if user:
        user = user_serialize_dict(user)
        user = user_schemas.User(**user)
        if user.isEmailVerified == False:
            db.users.find_one_and_update(
                {"uin": uin}, {"$set": {"isEmailVerified": True}}
            )
            return JSONResponse(
                {"message": "User activated"}, status_code=status.HTTP_200_OK
            )
        else:
            db.users.find_one_and_update(
                {"uin": uin}, {"$set": {"isEmailVerified": False}}
            )
            return JSONResponse(
                {"message": "User Deactivated"}, status_code=status.HTTP_200_OK
            )
    return JSONResponse(
        {"message": "No user with that uin"}, status_code=status.HTTP_404_NOT_FOUND
    )

# with open("/Users/progressive/Desktop/Projects/dojo-blog/data/db.json", "r") as f:
#     data = json.load(f)

# blogs = data["blogs"]
# @app.get('/blogs')
# async def get_blogs():
#     return blogs

# @app.get('/blogs/{id}')
# async def get_blogs(id: int):
#     return blogs[id-1]


add_pagination(app)
