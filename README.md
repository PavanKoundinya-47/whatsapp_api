# WhatsApp TMBC Bot (FastAPI)

## 🚀 Overview
A FastAPI app to send WhatsApp messages using Meta's WhatsApp Cloud API.

## 📬 Endpoint

GET /send_message?phone_number=+1234567890

## ✅ Requirements

- Python 3.8+
- Meta WhatsApp Cloud API Access

## 🔧 Setup
1. Clone the repo:

```bash
git clone https://github.com/your-repo/whatsapp-api.git
cd whatsapp-api
```

2.Install dependencies:
```bash
pip install -r requirements.txt
```

3.Edit config.py with your WhatsApp API credentials.

    for example, added my sample whatsapp number()


4.Run the server:

```
uvicorn main:app --reload
```

📱 Example Call
```
GET http://localhost:8000/send_message?phone_number=+1234567890
```