import requests 
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
        
        self.access_token = 'EAAPZBCStdBk0BOZCnn2er7D5HU9jjgERGRqGFe4dy6tZCNsYHIhLhGxr572MhO0kSKzfY2E7VF8FRCUVbt6sH6tZAPoSedK30Ycfjo6ZC3pVKa7v74dfSpLH77zUc9DsSgX8wKrsIdTJOnrRaPSIwlgEvXwAFO3QRGeAMHS8pZAjJVpSZCdluIMWylQr4ZCy567NJiylzIJmwwjKMAJFUZBiyoWSERVlmApTBXjMZD' 
        self.phone_number_id = '474660259071346'
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
        print(self.base_url) 
        
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
            raise Exception(str(e)) 
        
    def get_message(payload): 
        messages = payload["entry"][0]["changes"][0]["value"]["messages"] 
        message = [message["text"]["body"] for message in messages][0] 
        number = payload["entry"][0]["changes"][0]["value"]["messages"][0]["from"] 
        return number, message