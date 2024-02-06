import os
import sys

from fastapi import Request, FastAPI, HTTPException, APIRouter
from config.db import collection_image, collection_line

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
            
                message_text = data.get("result", [])
                if message_text:
                    message = TextSendMessage(text=message_text)
                    await line_bot_api.push_message(id, messages=message)
                    response = await line_bot_api.push_message(id, messages=message)
                    print(response.json())

                    collection_image.update_one({"_id": ObjectId(data["_id"])}, {"$set": {"status": True}})
        

