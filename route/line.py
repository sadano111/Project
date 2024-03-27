from fastapi import Request, HTTPException, APIRouter
from config.db import collection_image, collection_line, collection_express

from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx

from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage
)
from linebot.models import TextSendMessage

from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from bson import ObjectId
from urllib.parse import urlencode

from models.models import User, express,lineUser
from schemas.schemas import user_serializer, users_serializer, exPress_serializer, express_serializer, userToken_serializer, userTokens_serializer

# get channel_secret and channel_access_token from your environment variable
channel_secret = 'e3222b78675e0db46886176fadc83f61'
channel_access_token = 'VWOeAmz+Ps1FzV9GuXV42Tcp7Qa8yQ301/ZGeHGP+TFUC0dWnGWDs0fGQOQfESP6IGHqag+7P3yqOZUfc6+Cq6emmdmvd95naWvtg8rcIZ1lPjdTgdVFn1SPGDqYPJimxN58hfeEyojamcK0nE3adwdB04t89/1O/w1cDnyilFU='

configuration = Configuration(
    access_token=channel_access_token
)

line = APIRouter()
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
parser = WebhookParser(channel_secret)


@line.post("/push")
async def push_message():
    for data in collection_image.find():
        # เช็ค status ว่า line มีการแจ้งเตือนหรือยัง
        if data["status"] == False:

            # name = data["result"][0] + " " + data["result"][1]
            name = data["result"][0]
            line_id = collection_line.find_one({"name": name})

            if line_id:
                id = line_id["idToken"]
                print(id)
                await push(id, messages=[{"type":"text","text":"มีพัสดุมาส่ง"}])
                collection_image.update_one({"_id": ObjectId(data["_id"])}, {"$set": {"status": True}})
    return JSONResponse(content={"message": "OK"}, status_code=200)

async def push(to: str, messages: list[dict]):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer VWOeAmz+Ps1FzV9GuXV42Tcp7Qa8yQ301/ZGeHGP+TFUC0dWnGWDs0fGQOQfESP6IGHqag+7P3yqOZUfc6+Cq6emmdmvd95naWvtg8rcIZ1lPjdTgdVFn1SPGDqYPJimxN58hfeEyojamcK0nE3adwdB04t89/1O/w1cDnyilFU=",  # Replace with your Line API access token
    }
    body = {"to": to, "messages": messages}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.line.me/v2/bot/message/push", headers=headers, json=body
        )
        print(f"status = {response.status_code}")
        

# แปลง token ที่ได้เพื่อดูข้อมูล
async def verify(id_token:str):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    params = {
        'id_token': id_token,
        'client_id': '2004090496'
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.line.me/oauth2/v2.1/verify", headers=headers, params=urlencode(params)
        )
        json_response = response.json()
        return json_response

# บันทึกเฉพาะ userID 
@line.post("/id_token", tags=["line_user"])
async def post_users(data: lineUser):
    json_response = await verify(data.idToken)
    sub = json_response.get('sub')
    document = {"idToken": sub, "name": data.name}
    collection_line.insert_one(document)
    return {"status": "OK", "data":userTokens_serializer(collection_line.find())}

# ดูข้อมูลว่ามี user อะไรบ้าง
@line.get("/token", tags=["line_user"])
async def get_token():
    token = userTokens_serializer(collection_line.find())
    return {"status":"ok", "data":token}



class FollowEvent(BaseModel):
    type: str
    source: dict


@line.post("/callback")
async def callback(event: FollowEvent):
    if event.type == 'follow':
        # Extract user ID from the event
        user_id = event.source['userId']
        # Process the user ID (store it in the database, send a welcome message, etc.)
        # Your code here
    return {'message': 'OK'}


@line.get("/get_all_data")
async def get_all_data():
    users = users_serializer(collection_image.find())
    return {"status":"ok", "data":users}

@line.post("/express")
async def post_express(data:express):
    collection_express.insert_one(dict(data))
    return {"status":"ok", "data":exPress_serializer(collection_express.find())}

@line.get("/getdetail")
async def get_detail():
    detail = exPress_serializer(collection_express.find())
    return {"status":"ok", "data":detail}

@line.post("/post", tags=["user"])
async def post_users(user: lineUser):
    collection_line.insert_one(dict(user))
    return {"status": "OK"}



