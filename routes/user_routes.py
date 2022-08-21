from fastapi import APIRouter
import random

from models.user_models import User, SignIn, Number, LoginIn
from config.db import collection, collection_institutes
from schemas.user_schemas import userEntity, usersEntity

from bson import ObjectId
import requests
import json

from dotenv import load_dotenv
import os

load_dotenv()
FAST2SMS = os.getenv("FAST2SMS")
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
            return {"success": True, "data": {"name": user[0]['name'], "phone": user[0]['phone']}}
    else:
            return {"success": False}

@user.post('/get-otp')
async def get_otp(number: Number):
    otp = random.randint(1000,9999)
    url = "https://www.fast2sms.com/dev/bulk"
    my_data = {
        'sender_id': 'FSTSMS',
        'message': f'<#> {otp} 8JbtsPvGnRR',
        'language': 'english',
        'route': 'p',
        'numbers': number
    }

    headers = {
        'authorization': FAST2SMS,
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache"
    }

    response = requests.request("POST",
                                url,
                                data = my_data,
                                headers = headers)

    returned_msg = json.loads(response.text)

    return {"success": "ok", "data": returned_msg}

@user.get('/log-in')
async def login(logIn: LoginIn):
    user = collection_institutes.find_one({"udise_sch_code": logIn.udise, "password": logIn.password})
    if not user:
        return {"success": False, "data": []}
    elif user['udise_sch_code'] == logIn.udise and user['password'] == logIn.password:
        data = {
            "school_name": user['school_name'],
            "udise": user['udise_sch_code']
        }
        return {"success": True, "data": data}