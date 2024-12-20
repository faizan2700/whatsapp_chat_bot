import os
from fastapi import FastAPI, Request, HTTPException
import requests
from dotenv import load_dotenv 
from whatsapp_service import WhatsAppService 
from ai_agent import Assistant  
from fastapi.responses import HTMLResponse 




# Load environment variables
load_dotenv('./.env') 
# Create FastAPI app instance
app = FastAPI(title="WhatsApp Echo Bot")

# Initialize WhatsApp service
whatsapp_service = WhatsAppService()
ai_agent = Assistant() 
@app.post("/webhook")
async def handle_webhook(request: Request):
    body = request.json() 
    number, message = whatsapp_service.get_message(body)  
    # message = ai_agent.get_response(message) 
    response = whatsapp_service.send_message(number, message) 
    return {"status": "success", "response": response} 

@app.get("/webhook") 
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge") 
    if mode == "subscribe" and token == os.getenv("WHATSAPP_VERIFY_TOKEN"):
        return {"status": "success", "challenge": challenge}
    else:
        raise HTTPException(status_code=400, detail="Invalid request") 



@app.post("/send_message") 
async def send_message(message_request: Request):
    body = await message_request.json() 
    message = body.get("message") 
    to_number = body.get("to_number") 
    response = whatsapp_service.send_message(to_number, message) 
    return { "status": "success", "response": response }

@app.get('/home') 
async def home(request: Request): 
    return {'message': 'Hello World'} 
@app.get('/') 
async def hom1(request): 
    return HTMLResponse('<h1>Home</h1>', status_code=200)

# Main entry point for running the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)