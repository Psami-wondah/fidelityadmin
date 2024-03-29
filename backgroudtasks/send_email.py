from fastapi import BackgroundTasks
from db.config import db
from serializers.user_serializers import user_serialize_list
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_mail.errors import ConnectionErrors
from utils import config as settings
from schemas.user_schemas import UserEmail


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="templates",
)


# async def send_new_user_email():
#     count_check = db.user_count.find_one({"name": "counter"})
#     users_from_db = db.users.find()
#     users = user_serialize_list(users_from_db)
#     current_count = len(users)
#     if not count_check:
#         db.user_count.insert_one({"name": "counter", "count": current_count})

#     previous_count = db.user_count.find_one({"name": "counter"})["count"]
#     fm = FastMail(conf)
#     if current_count > previous_count:
#         difference = current_count - previous_count
#         new_user_list = users[-difference:]
#         db.user_count.find_one_and_update({"name": "counter"}, {'$set':{"count": current_count}})
#         for user in new_user_list:
#             user = UserEmail(**user)
#             message = MessageSchema(
#                 subject="A new user Joined Fidelity Trades",
#                 recipients=["okechukwusamuel16@gmail.com", "perrycharles282@gmail.com", "ellahokorie@gmail.com"],
#                 template_body={
#                     "uin": user.uin,
#                     "username": user.username,
#                     "email": user.email,
#                     "is_active": user.isEmailVerified,
#                     "name": user.username,
#                     "created_at": user.createdAt.strftime("%d %B, %Y %a. %I:%M %p"),
#                 },
#                 subtype="html",
#             )
            
#             await recursive_email_sending(fm=fm, test_message=message)
    
    

# async def recursive_email_sending(fm: FastMail, test_message):
#     try:
#         await fm.send_message(test_message, template_name="new_user_template.html")
#     except ConnectionErrors:
#         await recursive_email_sending(fm, test_message)



    
