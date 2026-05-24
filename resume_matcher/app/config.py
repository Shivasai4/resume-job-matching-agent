import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    embedding_model: str = "nomic-embed-text"   # or "all-minilm:latest"
    llm_model: str =  "llama3.2:latest" # or "mistral"
    max_retries: int = 3
    retry_delay: float = 1.0
    log_level: str = "INFO"
    # Langfuse
    langfuse_public_key: str = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    langfuse_secret_key: str = os.getenv("LANGFUSE_SECRET_KEY", "")
    langfuse_host: str = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

settings = Settings()