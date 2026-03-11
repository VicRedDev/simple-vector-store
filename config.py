from dotenv import load_dotenv
load_dotenv(override = True)
import os

SCAPE_KEYWORD = os.getenv('SCAPE_KEYWORD', '/bye')

PROCESSING_LIMIT = os.getenv('PROCESSING_LIMIT', False)
MULTI_PROCESSING_LIMIT = os.getenv('MULTI_PROCESSING_LIMIT', 1)

VECTORSTORE_PATH = os.getenv('VECTORSTORE_PATH', 'embeddings')

EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', False)
EMBEDDING_API_KEY = os.getenv('EMBEDDING_API_KEY', False)
EMBEDDING_BASE_URL = os.getenv('EMBEDDING_BASE_URL', False)

CHAT_MODEL = os.getenv('CHAT_MODEL', False)
CHAT_API_KEY = os.getenv('CHAT_API_KEY', False)
CHAT_BASE_URL = os.getenv('CHAT_BASE_URL', False)