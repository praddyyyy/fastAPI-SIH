from email import message
from fastapi import APIRouter

from models.user_models import User, SignIn
from config.db import collection
from schemas.user_schemas import userEntity, usersEntity

from bson import ObjectId

user = APIRouter()

@user.get('/')
async def root():
    return {"status": "ok", "message": "FastAPI"}

@user.get('/find-users')
async def find_all_users():
    users = usersEntity(collection.find())
    return {"status": "ok", "data": users}

@user.get('/find-user-id/{id}')
async def get_user(id: str):
    user = usersEntity(collection.find({"aadhar_no": id}))
    return {"status": "ok", "data": user}

@user.post('/create-user')
async def create_user(user: User):
    _id = collection.insert_one(dict(user))
    user = usersEntity(collection.find({"_id": _id.inserted_id}))
    return {"status": "ok", "data": user}

@user.put('/update-user-id/{id}')
async def update_user(id: str, user: User):
    collection.find_one_and_update({"aadhar_no": id}, {
        "$set": dict(user)
    })
    user = usersEntity(collection.find({"aadhar_no": id}))
    return {"status": "ok", "data": user}

@user.delete('/delete-user-id/{id}')
async def delete_user(id: str):
    user = collection.find_one_and_delete({"aadhar_no": id})
    return {"status": "ok", "data": []}

@user.post('/sign-in')
async def sign_in(signIn: SignIn):
    user = usersEntity(collection.find({"aadhar_no": signIn.aadhar_no, "email": signIn.email}))
    if len(user)>0:
        if user[0]['aadhar'] == signIn.aadhar_no and user[0]['email'] == signIn.email:
            return {"success": True}
    else:
        return {"success": False}