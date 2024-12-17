import requsts 
import os 
import dotenv  
import requests


class WhatsAppService:
    """
    Service responsible for handling WhatsApp messaging operations.
    This follows the Single Responsibility Principle by encapsulating 
    WhatsApp API communication logic.
    """
    def __init__(self):
        dotenv.load_dotenv() 
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
            raise Exception(status_code=500, detail="Failed to send WhatsApp message")