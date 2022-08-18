from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    aadhar_no: str

class SignIn(BaseModel):
    email: str
    aadhar_no: str
