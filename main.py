from fastapi import FastAPI
from route.upload import route
from OCR.ocr import ocr_router
from route.line import line
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# app.include_router(route) ไม่ได้ใช้
app.include_router(ocr_router)
app.include_router(line)

# Enable CORS (Cross-Origin Resource Sharing) for all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

