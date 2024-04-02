from pydantic import BaseModel

class User(BaseModel):
    filename: int
    result: str
    status: int

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
    roles: bool