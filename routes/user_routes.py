from fastapi import APIRouter
import random

from models.user_models import User, SignIn, Number, LoginIn, AadhaarUser
from config.db import collection, collection_institutes, collection_aadhaar
from schemas.user_schemas import usersEntity, aadhaarsEntity

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
async def update_user(id: str, udise: dict):
    collection.find_one_and_update({"aadhar_no": id}, {
        "$set": udise
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

@user.post('/get-otp/{aid}')
async def get_otp(number: Number, aid):
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

    collection_aadhaar.find_one_and_update({"aadhaar": aid}, {
        "$set": {"otp": otp}
    })

    return {"success": "ok", "data": returned_msg, "otp": otp}

@user.put('/verify-otp/{aid}/{otp}')
async def verify_otp(aid: str, otp: int):
    user = collection_aadhaar.find_one({"aadhaar": aid, "otp": otp})
    if user:
        collection_aadhaar.find_one_and_update({"aadhaar": aid}, {
            "$unset": {"otp": otp}
        })
        return {"success":"ok"}
    elif not user:
        return {"success": "not ok"}
    

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

@user.get('/find-user-udise/{code}')
async def get_user(code):
    user = usersEntity(collection.find({"institute_id": code, "tc": False}))
    return {"status": "ok", "data": user}

@user.put('/update-user-tc-false/{id}')
async def update_user(id: str):
    collection.find_one_and_update({"aadhar_no": id}, {
        "$set": {"tc": False}
    })
    user = usersEntity(collection.find({"aadhar_no": id}))
    return {"status": "ok", "data": user}

@user.put('/update-user-tc/{id}')
async def update_user(id: str):
    collection.find_one_and_update({"aadhar_no": id}, {
        "$set": {"tc": True}
    })
    user = usersEntity(collection.find({"aadhar_no": id}))
    return {"status": "ok", "data": user}

@user.put('/update-user-many/{id}')
async def update_user(id: str, data: dict):
    collection.find_one_and_update({"aadhar_no": id}, {
        "$push": {'academic_details': data}
    })
    user = usersEntity(collection.find({"aadhar_no": id}))
    return {"status": "ok", "data": user}

@user.get('/find-phone/{id}')
async def find_phone(id: str):
    user = collection_aadhaar.find_one({"aadhaar": id})
    if user:
        return {"status": True, "phone": user['phone']}
    else:
        return {"status": False, "phone": []}

@user.post('/create-aadhaar-user')
async def create_user(user: AadhaarUser):
    _id = collection_aadhaar.insert_one(dict(user))
    user = aadhaarsEntity(collection_aadhaar.find({"_id": _id.inserted_id}))
    return {"status": "ok", "data": user}

@user.put('/last/{id}/{doj}/{dol}')
async def last(id:str, doj:str, dol:str):
    collection.find_one_and_update({"aadhar_no": id, "academic_details.doj": doj}, {
        "$set": {"academic_details.$.dol": dol}
    })

    return {"status": "ok"}

@user.get('/ekyc/{aid}')
async def ekyc(aid):
    user = collection_aadhaar.find_one({"aadhaar": aid})
    return {"status": "ok", "data": {"name": user['name'], "phone": user['phone']}}