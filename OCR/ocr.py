# import cv2
# import easyocr

# image = cv2.imread(r'C:\Users\Admin\Desktop\project\image\parcel\flash\1.jpg')
# # cv2.imshow('image',image)

# image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# # cv2.imshow('image_gray',image_gray)

# image_wb = cv2.threshold(image_gray, 100, 255, cv2.THRESH_BINARY)[1]
# cv2.imshow('image_wb', image_wb)

# reader = easyocr.Reader(['th'],gpu = True)
# result = reader.readtext(image_wb,detail=0)
# print(result)

# cv2.waitKey(0)
# cv2.destroyAllWindows

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from config.db import collection_image
from typing import List
import cv2
import easyocr
import numpy as np

ocr_router = APIRouter()

def process_ocr(image_content):
    # Convert image content to numpy array
    nparr = np.frombuffer(image_content, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Perform OCR
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_wb = cv2.threshold(image_gray, 100, 255, cv2.THRESH_BINARY)[1]
    reader = easyocr.Reader(['th'], gpu=True)
    position = image_wb[740:764,681:1000] # [Y,X] 681,740  /  686,791  / 1000,719  / 1000 764
    result = reader.readtext(position, detail=0)
    # result = reader.readtext(image_wb, detail=0)
    return result

@ocr_router.post("/perform-ocr-multiple/")
async def perform_ocr_multiple(files: List[UploadFile] = File(...)):
    try:
        ocr_results = []
        for file in files:
            image_content = await file.read()
            ocr_result = process_ocr(image_content)
            ocr_results.append({"filename": file.filename, "result": ocr_result})
            collection_image.insert_one({"filename": file.filename, "result": ocr_result, "status":False})

        return JSONResponse(content={"results": ocr_results}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
