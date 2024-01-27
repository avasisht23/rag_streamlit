import qdrant_client
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.service_context import ServiceContext


class QdrantClient(object):
    def __init__(self, collection_name: str, url: str = "http://localhost:6333"):
        self.inner = qdrant_client.QdrantClient(url=url)
        self.service_context = ServiceContext.from_defaults()
        self.vector_store = QdrantVectorStore(
            client=self.inner, collection_name=collection_name
        )
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )
