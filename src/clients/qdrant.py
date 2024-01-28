import qdrant_client
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.service_context import ServiceContext

from utils.constants import LOCAL_QDRANT_URL


class QdrantClient(object):
    def __init__(self, api_key: str = None, url: str = LOCAL_QDRANT_URL):
        if url != LOCAL_QDRANT_URL and api_key is None:
            raise ValueError(
                "Qdrant API key must be provided if not using local Qdrant instance."
            )

        self.inner = qdrant_client.QdrantClient(url=url, api_key=api_key)
        self.service_context = ServiceContext.from_defaults()
        self.vector_store = None
        self.storage_context = None

    def build_vector_store(self, collection_name: str):
        """
        Builds a vector store for the given collection name.

        Args:
            collection_name (str): The name of the collection to build a vector store for.
        """

        self.vector_store = QdrantVectorStore(
            client=self.inner, collection_name=collection_name
        )
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )
