from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    number: int
    phone: str
    name: str
    date: datetime
    company: str
    take: bool

class parcel(BaseModel):
    to: str


class lineUser(BaseModel):
    idToken: str
    name: str
    
class express(BaseModel):
    name: str
    phone: int
    role: str
    express: str
    parcel: int

class userAccount(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    roles: str

class ocr(BaseModel):
    number: str
    phone: str
    name: str
    company: str
    status: bool
    take: bool
