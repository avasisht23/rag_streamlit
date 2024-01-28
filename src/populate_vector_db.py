import os
from dotenv import load_dotenv
from llama_index import SimpleDirectoryReader, VectorStoreIndex
from qdrant_client.models import CollectionStatus

from clients.qdrant import QdrantClient
from utils.constants import EARNINGS_CALLS_REL_DIRNAME, LOCAL_QDRANT_URL
from utils.parsing import parse_earnings_calls


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")

if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY not found in environment variables")

if not QDRANT_URL:
    QDRANT_URL = LOCAL_QDRANT_URL
    QDRANT_API_KEY = None

print(f"Populating Vector DB in URL {QDRANT_URL} with API KEY {QDRANT_API_KEY}")

parsed_earnings_calls = parse_earnings_calls(EARNINGS_CALLS_REL_DIRNAME)

print("Parsed earnings calls")

for stock_symbol, files in parsed_earnings_calls.items():
    collection_name = f"earnings_calls_{stock_symbol}"
    company_documents = SimpleDirectoryReader(input_files=files).load_data()

    qdrant_client = QdrantClient(api_key=QDRANT_API_KEY, url=QDRANT_URL)
    qdrant_client.build_vector_store(collection_name=collection_name)

    try:
        collection = qdrant_client.inner.get_collection(collection_name)
        if collection.status != CollectionStatus.GREEN:
            qdrant_client.inner.delete_collection(collection_name)
            raise Exception(f"Collection {collection_name} not found")

        print(f"Collection {collection_name} found, don't need to add it")
        company_index = VectorStoreIndex.from_vector_store(
            vector_store=qdrant_client.vector_store,
            service_context=qdrant_client.service_context,
            storage_context=qdrant_client.storage_context,
        )
    except Exception:
        print(f"Collection {collection_name} not found, adding it now")
        company_index = VectorStoreIndex.from_documents(
            company_documents,
            service_context=qdrant_client.service_context,
            storage_context=qdrant_client.storage_context,
        )

print("Populated Vector DB with collections by stock symbol via earnings calls")
