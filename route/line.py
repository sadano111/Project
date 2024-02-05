import os
import sys

from fastapi import Request, FastAPI, HTTPException, APIRouter
from config.db import collection_image

from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)


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


    # for data in collection_image.find():
    #     if data["status"] == False:



# ตรงนี้เป็นการวนลูป event ในการตอบกลับผู้ใช้
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessageContent):
            continue

        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

    return 'OK'