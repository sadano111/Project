from fastapi import FastAPI
from route.upload import route
from OCR.ocr import ocr_router
from route.line import line
from route.login import login
from fastapi.middleware.cors import CORSMiddleware
from config.db import collection_line, collection_image
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# app.include_router(route) ไม่ได้ใช้แล้ว
app.include_router(ocr_router)
app.include_router(line)
app.include_router(login)

# Enable CORS (Cross-Origin Resource Sharing) for all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

