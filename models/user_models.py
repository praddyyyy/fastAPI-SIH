from pydantic import BaseModel
from typing import Dict, List
class AcademicDetail(BaseModel):
    institution_name: str
    course: str
    doj: str
    dol: str
class User(BaseModel):
    aadhar_no: str
    tc: bool
    institute_id: str
    name: str
    email: str
    gender: str
    phone: str
    birthdate: str
    parent_mail: str
    academic_details: List[Dict]
    parent_approval: str
class SignIn(BaseModel):
    email: str
    aadhar_no: str

class Number(BaseModel):
    number: str

#login model for institutions
class LoginIn(BaseModel):
    udise: str
    password: str

class AadhaarUser(BaseModel):
    aadhaar: str
    name: str
    phone: str