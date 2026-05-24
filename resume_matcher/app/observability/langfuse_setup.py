from langfuse import Langfuse
from langfuse.callback import CallbackHandler
from app.config import settings
import logging

logger = logging.getLogger(__name__)
langfuse_handler = None

def init_langfuse():
    global langfuse_handler
    if settings.langfuse_public_key and settings.langfuse_secret_key:
        try:
            langfuse = Langfuse(
                public_key=settings.langfuse_public_key,
                secret_key=settings.langfuse_secret_key,
                host=settings.langfuse_host
            )
            langfuse_handler = CallbackHandler()
            logger.info("Langfuse initialized")
        except Exception as e:
            logger.warning(f"Langfuse init failed, tracing disabled: {e}")
    else:
        logger.info("Langfuse keys not set; tracing disabled")