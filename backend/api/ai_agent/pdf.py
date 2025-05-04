import os
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)
from llama_index.readers.file.docs.base import PDFReader

def get_index(data, index_name):
    index = None
    if not os.path.exists(index_name):
        print("Building index...", index_name)
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index= load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_name)
        )

    return index

date_dir = os.path.join(os.path.dirname(__file__), 'data')

united_states_pdf_path = os.path.join(date_dir, "United_States.pdf")
world_population_pdf_path = os.path.join(date_dir, "WorldPopulation.pdf")
kaleb_pdf_path = os.path.join(date_dir, "KalebResume.pdf")

United_States = PDFReader().load_data(file=united_states_pdf_path)
World_Population = PDFReader().load_data(file=world_population_pdf_path)
kaleb_resume = PDFReader().load_data(file=kaleb_pdf_path)

United_index = get_index(United_States, "United_States")
World_index = get_index(World_Population, "World_Population")
kaleb_index = get_index(kaleb_resume, "kaleb_resume")

United_engine = United_index.as_query_engine()
World_engine = World_index.as_query_engine()
Kaleb_engine = kaleb_index.as_query_engine()
