from fastapi import FastAPI, HTTPException, Query
import re
from fastapi.responses import FileResponse
import os
from whatsapp import send_whatsapp_message

app = FastAPI()

# Regex to validate E.164 phone number (e.g., +1234567890)
PHONE_REGEX = re.compile(r"^\+?\d{10,15}$")

IMAGE_DIRECTORY = "images"


@app.get("/images/{image_name}")
async def get_image(image_name: str):
    image_path = os.path.join(IMAGE_DIRECTORY, image_name)

    # Check if the image exists
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        return {"error": "Image not found"}
    



@app.get("/send_message")
async def send_message(phone_number: str = Query(..., description="Phone number in E.164 format (e.g. +1234567890 or 1234567890)")):
    phone_number = phone_number.strip().replace(" ", "")

    if not PHONE_REGEX.match(phone_number):
        raise HTTPException(
            status_code=400,
            detail="Invalid phone number format. Use digits only, optionally starting with +, 10-15 digits total."
        )

    # Normalize: Remove '+' if present (WhatsApp API wants raw digits)
    normalized_number = phone_number.lstrip("+")

    try:
        response = send_whatsapp_message(normalized_number)
        return {"status": "success", "response": response}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
