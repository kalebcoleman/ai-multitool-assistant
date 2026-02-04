import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.llms.google_genai import GoogleGenAI

# Load environment variables from backend/.env
backend_dir = Path(__file__).resolve().parent.parent.parent
load_dotenv(backend_dir / ".env")


@lru_cache(maxsize=1)
def get_llm():
    """Create and cache the Google GenAI LLM instance."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. Add it to backend/.env before starting the server."
        )

    model = os.getenv("GOOGLE_GENAI_MODEL", "gemini-2.5-flash")
    try:
        return GoogleGenAI(model=model, api_key=api_key)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"Failed to initialize Google GenAI model '{model}'. {exc}"
        ) from exc


@lru_cache(maxsize=1)
def _get_embed_model():
    try:
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            "HuggingFace embeddings are unavailable. Ensure torch, torchvision, "
            "transformers, and sentence-transformers are installed in this environment."
        ) from exc
    return HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")


def init_llama_settings():
    """Initialize LlamaIndex settings once."""
    Settings.embed_model = _get_embed_model()
    Settings.llm = get_llm()
