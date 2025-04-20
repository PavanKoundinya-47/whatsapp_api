from fastapi import FastAPI, HTTPException, Query
import re
from whatsapp import send_whatsapp_message

app = FastAPI()

# E.164 phone number regex pattern
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

@app.get("/send_message")
async def send_message(phone_number: str = Query(..., description="E.164 format: +1234567890")):
    if not PHONE_REGEX.match(phone_number):
        raise HTTPException(status_code=400, detail="Invalid phone number format. Use E.164 format, e.g. +1234567890")

    try:
        response = send_whatsapp_message(phone_number)
        return {"status": "success", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
