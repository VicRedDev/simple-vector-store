from config import EMBEDDING_API_KEY, EMBEDDING_BASE_URL, EMBEDDING_MODEL, CHAT_API_KEY, CHAT_BASE_URL, CHAT_MODEL
from openai import OpenAI

class AI:
    def __init__(self):
        if EMBEDDING_BASE_URL:
            self.embeddings_client = OpenAI(base_url = EMBEDDING_BASE_URL, api_key = EMBEDDING_API_KEY)
            self.embeddings_model = EMBEDDING_MODEL
        else:
            self.embeddings_client = OpenAI(api_key = EMBEDDING_API_KEY)
            self.embeddings_model = EMBEDDING_MODEL
            
        if CHAT_BASE_URL:
            self.chat_client = OpenAI(base_url = CHAT_BASE_URL, api_key = CHAT_API_KEY)
            self.chat_model = CHAT_MODEL
        else:
            self.chat_client = OpenAI(api_key = CHAT_API_KEY)
            self.chat_model = CHAT_MODEL

    def response(self, messages):
        try:
            completion = self.chat_client.chat.completions.create(
                messages = messages,
                model = self.chat_model,
            ).choices[0]
            return completion.message
        except:
            return False
        
    def embed(self, text):
        try:
            embeddings_result = self.embeddings_client.embeddings.create(
                input = text,
                model = self.embeddings_model,
                encoding_format = 'float',
            )
            embeddings = embeddings_result.data[0].embedding
            return embeddings
        except:
            return False