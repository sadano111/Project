# ข้อมูลสำหรับผู้รับพัสดุ
def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "filename": user["filename"],
        "result": user["result"],
        "status": user["status"]
    }

def users_serializer(users) -> list:
    return [user_serializer(user) for user in users]

# ข้อมูลสำหรับผู้ส่งพัสดุ
def express_serializer(item) -> dict:
    return{
        "id": str(item["_id"]),
        "name": item["name"],
        "phone": item["phone"],
        "role": item["role"],
        "express": item["express"],
        "parcel": item["parcel"]
    }

def exPress_serializer(items) -> list:
    return [express_serializer(item) for item in items]

# get ผู้รับ
def parcel_serializer(item) -> dict:
    return{
        "id": str(item["_id"]),
        "name": item["name"]
    }

def parcels_serializer(items) -> list:
    return [parcel_serializer(item) for item in items]
    
# id_token from line
def userToken_serializer(item) -> dict:
    return {
        "id": str(item["_id"]),
        "idToken": item["idToken"],
        "name": item["name"]
    }

def userTokens_serializer(items) -> list:
    return [userToken_serializer(item) for item in items]

def loginUser_serializer(item) -> dict:
    return {
        "id": str(item["_id"]),
        "username": item["username"],
        "password": item["password"],
        "firstname": item["firstname"],
        "lastname": item["lastname"]
    }

def loginUsers_serializer(items) -> list:
    return [loginUser_serializer(item) for item in items]
