import os
from functools import lru_cache
from pathlib import Path

from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.readers.file.docs.base import PDFReader

from .llm import get_llm, init_llama_settings

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def get_index(data, index_dir):
    """Load or create a vector index for the given documents."""
    index = None
    if not os.path.exists(index_dir):
        print(f"Building index: {index_dir}...")
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_dir)
    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_dir)
        )
    return index


@lru_cache(maxsize=1)
def _load_pdf_documents():
    """Load static PDF documents from disk once."""
    united_states_pdf_path = DATA_DIR / "United_States.pdf"
    world_population_pdf_path = DATA_DIR / "WorldPopulation.pdf"
    kaleb_pdf_path = DATA_DIR / "KalebResume.pdf"

    return {
        "united": PDFReader().load_data(file=str(united_states_pdf_path)),
        "world": PDFReader().load_data(file=str(world_population_pdf_path)),
        "kaleb": PDFReader().load_data(file=str(kaleb_pdf_path)),
    }


@lru_cache(maxsize=1)
def get_pdf_engines():
    """Return cached query engines for static PDFs."""
    init_llama_settings()
    llm = get_llm()

    documents = _load_pdf_documents()

    united_index = get_index(documents["united"], str(BASE_DIR / "United_States"))
    world_index = get_index(documents["world"], str(BASE_DIR / "World_Population"))
    kaleb_index = get_index(documents["kaleb"], str(BASE_DIR / "kaleb_resume"))

    return {
        "united": united_index.as_query_engine(llm=llm),
        "world": world_index.as_query_engine(llm=llm),
        "kaleb": kaleb_index.as_query_engine(llm=llm),
    }
