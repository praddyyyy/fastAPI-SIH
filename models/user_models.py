from pydantic import BaseModel
from typing import List
class AcademicDetail(BaseModel):
    college: str
    university: str
    course: str
    doj: str
    dol: str
class User(BaseModel):
    aadhar_no: str
    tc: str
    institute_type: str
    institute_id: str
    name: str
    email: str
    gender: str
    phone: str
    birthdate: str
    academic_details: List[AcademicDetail]
class SignIn(BaseModel):
    email: str
    aadhar_no: str

class Number(BaseModel):
    number: str