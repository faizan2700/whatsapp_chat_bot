from transformers import pipeline 

class Assistant: 
    """
    A conversational AI agent that leverages a pre-trained language model
    to provide responses to user queries.
    """
    def __init__(self, model_name: str = "facebook/blenderbot-400M-distill"):
        """
        Initialize the assistant with a pre-trained language model.

        Args:
            model_name (str): Name of the pre-trained model to use. 
        Default is "facebook/blenderbot-400M-distill". 
        """ 
        self.model = pipeline("text2text-generation", model=model_name) 
    def get_response(self, user_input: str) -> str:
        """
        Generate a response to the user's input using the pre-trained model. 
        Args:
            user_input (str): The user's input query.

        Returns:
            str: The AI-generated response.
        """ 
        return self.model(user_input) 
    
if __name__=='__main__': 
    assistant = Assistant()
    while True:
        user_input = input("You: ")
        response = assistant.get_response(user_input) 
        try: 
            print(f"AI: {response[0].get('generated_text')}") 
        except Exception as error: 
            print(f'AI unavailable: {error}') 