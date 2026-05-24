import ollama
import logging
import time
from app.config import settings
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

logger = logging.getLogger(__name__)

class Embedder:
    def __init__(self):
        self.client = ollama.Client(host=settings.ollama_base_url)
        self.model = settings.embedding_model

    @retry(
        stop=stop_after_attempt(settings.max_retries),
        wait=wait_fixed(settings.retry_delay),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
        reraise=True
    )
    def embed(self, text: str) -> list[float]:
        try:
            response = self.client.embeddings(model=self.model, prompt=text)
            return response['embedding']
        except Exception as e:
            logger.error(f"Embedding failed: {e}")
            raise