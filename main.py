import os
from fastapi import FastAPI, Request, HTTPException
import requests
from dotenv import load_dotenv

# Import our custom models
from whatsapp_models import (
    WhatsAppWebhookPayload, 
    MessageResponse
)

# Load environment variables
load_dotenv()

# Create FastAPI app instance
app = FastAPI(title="WhatsApp Echo Bot")

class WhatsAppService:
    """
    Service responsible for handling WhatsApp messaging operations.
    This follows the Single Responsibility Principle by encapsulating 
    WhatsApp API communication logic.
    """
    def __init__(self):
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
        self.base_url = f"https://graph.facebook.com/v21.0/{self.phone_number_id}/messages"
        
        if not all([self.access_token, self.phone_number_id]):
            raise ValueError("WhatsApp API credentials are not fully configured")
    
    def send_message(self, to_number: str, message_body: str) -> dict:
        """
        Send a message via WhatsApp API.
        
        Args:
            to_number (str): Recipient's phone number
            message_body (str): Message content to send
        
        Returns:
            dict: Response from WhatsApp API
        """
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_number,
            "type": "text",
            "text": {"body": message_body}
        }
        
        try:
            response = requests.post(
                self.base_url, 
                json=payload, 
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error sending message: {e}")
            raise HTTPException(status_code=500, detail="Failed to send WhatsApp message")

# Initialize WhatsApp service
whatsapp_service = WhatsAppService()

@app.post("/webhook")
async def handle_webhook(payload: WhatsAppWebhookPayload):
    """
    Webhook endpoint to receive and process WhatsApp messages.
    
    This method follows the Open/Closed Principle by being 
    open for extension (easy to add more complex logic) 
    but closed for modification.
    
    Args:
        payload (WhatsAppWebhookPayload): Incoming webhook payload
    
    Returns:
        dict: Acknowledgement of message processing
    """
    # Validate payload and extract message details
    if payload.object != "whatsapp_business_account":
        raise HTTPException(status_code=400, detail="Invalid webhook payload")
    
    for entry in payload.entry:
        for change in entry.changes:
            if change.field == "messages":
                messages = change.value.get("messages", [])
                for msg in messages:
                    if msg.get("type") == "text":
                        # Echo back the same message
                        sender_number = msg.get("from", "")
                        message_body = msg.get("text", {}).get("body", "")
                        
                        # Send response using WhatsApp service
                        whatsapp_service.send_message(
                            to_number=sender_number, 
                            message_body=message_body
                        )
    
    return {"status": "success"}

@app.get("/webhook")
def verify_webhook(request: Request):
    """
    Verify webhook endpoint for initial setup with WhatsApp API.
    
    Args:
        request (Request): Incoming HTTP request
    
    Returns:
        str: Verification token or challenge
    """
    hub_mode = request.query_params.get('hub.mode')
    hub_challenge = request.query_params.get('hub.challenge')
    hub_verify_token = request.query_params.get('hub.verify_token')
    
    # Add your actual verification token logic here
    if hub_mode == 'subscribe' and hub_challenge:
        return hub_challenge
    
    raise HTTPException(status_code=403, detail="Verification failed") 

@app.post("/send_message") 
async def send_message(message_request: MessageResponse):
    message = message_request.message 
    to_number = message_request.to_number 
    response = whatsapp_service.send_message(to_number, message) 
    return { "status": "success", "response": response }

# Main entry point for running the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)