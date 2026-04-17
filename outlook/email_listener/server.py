# installed pip install fastapi uvicorn
# enter on terminal ngrok config add-authtoken YOUR_AUTHTOKEN_HERE

# run  uvicorn server:app --port 8000 on terminal 1
# run ngrok http 8000 on terminal 2, make sure to copy paste this url to power atuomate

from fastapi import FastAPI, Request

app = FastAPI()

# This is the endpoint that Power Automate will send data to
@app.post("/webhook")
async def receive_email(request: Request):
    # Extract the JSON data sent by Power Automate
    payload = await request.json()
    
    sender = payload.get("sender")
    subject = payload.get("subject")
    
    print("\n--- INCOMING WEBHOOK ---")
    print(f"Received email from: {sender}")
    print(f"Subject: {subject}")
    print("------------------------\n")
    
    # You must return a 200 OK status so Power Automate knows it succeeded
    return {"status": "success", "message": "Webhook received"}

