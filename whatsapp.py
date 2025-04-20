import requests
from config import WHATSAPP_API_URL, ACCESS_TOKEN, PHONE_NUMBER_ID

def send_whatsapp_message(to_number: str):
    url = f"{WHATSAPP_API_URL}/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            },
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "image",
                            "image": {
                                "link": "http://localhost:8000/images/my_image.jpg"
                            }
                        }
                    ]
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        try:
            error_json = response.json()
            error_data = error_json.get("error", {})
            code = error_data.get("code", 0)
            message = error_data.get("message", "")
            detail = error_data.get("error_data", {}).get("details", "")

            if code == 131030 and "not in allowed list" in message:
                raise Exception(
                    f"The number {to_number} is not in the test recipients list. "
                    "Please add it via the WhatsApp Business Manager and verify it manually."
                )
            elif code == 132001 and "Template name" in message:
                raise Exception(
                    f"Template '{payload['template']['name']}' does not exist for language '{payload['template']['language']['code']}'. "
                    f"Please verify that the template is approved and has the correct language (e.g. en_US). Meta details: {detail}"
                )
            else:
                raise Exception(f"WhatsApp API Error {code}: {message} — {detail or 'No further details'}")
        except ValueError:
            raise Exception(f"Failed to send message and parse error response: {response.text}")

    return response.json()
