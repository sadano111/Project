import os
import sys

from fastapi import Request, HTTPException, APIRouter
from config.db import collection_image, collection_line

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


class LinePush(BaseModel):
    to: str
    messages: list[dict]

# @line.post("/push")
# async def push_message(payload: LinePush):
#     await push(payload.to, payload.messages)
#     return JSONResponse(content={"message": "OK"}, status_code=200)

@line.post("/push")
async def push_message():
    # เพิ่มเงื่อนไขในการ push ตรงนี้
    for data in collection_image.find():
        # เช็ค status ว่า line มีการแจ้งเตือนหรือยัง
        if data["status"] == False:

            name = data["result"][0] + " " + data["result"][1]
            line_id = collection_line.find_one({"name": name})

            if line_id:
                id = line_id["line"]
                await push(id, messages=[{"type":"text","text":"มีพัสดุมาส่ง"}])
                collection_image.update_one({"_id": ObjectId(data["_id"])}, {"$set": {"status": True}})

    # **************************
    # await push(payload.to, payload.messages)
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


@line.post("/callback")
async def handle_callback(request: Request):
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = await request.body()
    body = body.decode()

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")


    for data in collection_image.find():
        # เช็ค status ว่า line มีการแจ้งเตือนหรือยัง
        if data["status"] == False:

            name = data["result"][0] + " " + data["result"][1]
            line_id = collection_line.find_one({"name": name})

            if line_id:
                id = line_id["line"]
            
                message_text = "มีพัสดุอยู่ที่ห้อง"
                message = TextSendMessage(text=message_text)
                line_bot_api.push_message(id, messages=[message])

                collection_image.update_one({"_id": ObjectId(data["_id"])}, {"$set": {"status": True}})
    return 'ok'

# @line.get("/get_test")
# async def get():
    
#     for data in collection_image.find():
#         name = data["result"][0] + " " + data["result"][1]
#         print(name)
#         line_id = collection_line.find_one({"name": name})
#         print(line_id)
#         id = line_id["line"]
#         print(id)
#     return {"status": "OK"}
