from pydantic import BaseModel

class User(BaseModel):
    filename: int
    result: str
    status: int

class parcel(BaseModel):
    to: str


class express(BaseModel):
    name: str
    phone: str
    role: str
    express: str
    parcel: int

class lineUser(BaseModel):
    idToken: str
    name: str

class userAccount(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
