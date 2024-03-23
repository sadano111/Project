from pydantic import BaseModel

class User(BaseModel):
    filename: int
    result: str
    status: int

class parcel(BaseModel):
    to: str


class lineUser(BaseModel):
    userId: str
    displayName: str
    

class express(BaseModel):
    name: str
    phone: int
    role: str
    express: str
    parcel: int
