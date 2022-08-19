from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    aadhar_no: str
    phone: str
    birthdate: str
    college: str
    gender: str
    course: str
    admission: str
    university: str
    institute_type: str
    institute_id: str
    tc: str
    doj: str
    dol: str

class SignIn(BaseModel):
    email: str
    aadhar_no: str

class Number(BaseModel):
    number: str