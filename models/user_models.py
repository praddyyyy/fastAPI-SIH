from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    aadhar_no: str
