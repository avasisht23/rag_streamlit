import os
from llama_index import Document
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.query_engine import SubQuestionQueryEngine
from llama_index.indices import VectorStoreIndex
from llama_index.readers import SimpleDirectoryReader
from qdrant_client.models import CollectionStatus

from clients.qdrant import QdrantClient
from utils.parsing import parse_earnings_calls
from utils.constants import EARNINGS_CALLS_REL_DIRNAME, LOCAL_QDRANT_URL


class LlamaIndexClient(object):
    def __init__(
        self,
        openai_api_key: str,
        qdrant_api_key: str,
        qdrant_url: str = LOCAL_QDRANT_URL,
    ):
        os.environ["OPENAI_API_KEY"] = openai_api_key
        self.qdrant_api_key = qdrant_api_key
        self.qdrant_url = qdrant_url

        self.engine = None

    def build_engine(self, dirname: str = EARNINGS_CALLS_REL_DIRNAME):
        """
        Builds the query engine with the earnings calls data.

        Args:
            dirname (str): The directory containing the earnings calls.
        """
        query_engine_tools = []

        parsed_earnings_calls = parse_earnings_calls(dirname)
        for stock_symbol, files in parsed_earnings_calls.items():
            collection_name = f"earnings_calls_{stock_symbol}"
            company_documents = SimpleDirectoryReader(input_files=files).load_data()

            qdrant_client = QdrantClient(
                api_key=self.qdrant_api_key, url=self.qdrant_url
            )
            qdrant_client.build_vector_store(collection_name=collection_name)

            company_index = self.__build_index(
                qdrant_client, collection_name, company_documents
            )

            company_query_engine = company_index.as_query_engine()
            query_engine_tool = QueryEngineTool(
                query_engine=company_query_engine,
                metadata=ToolMetadata(
                    name=collection_name,
                    description=f"Provides information about earnings calls for the company with stock symbol: {stock_symbol}",
                ),
            )

            query_engine_tools.append(query_engine_tool)

        self.engine = SubQuestionQueryEngine.from_defaults(
            query_engine_tools=query_engine_tools, use_async=False
        )

    def __build_index(
        self,
        qdrant_client: QdrantClient,
        collection_name: str,
        company_documents: [Document],
    ):
        """
        Builds the index for the given company.

        Args:
            qdrant_client (QdrantClient): The Qdrant client to use.
            collection_name (str): The name of the collection to build.
            company_documents ([Document]): The list of documents to use to build the index.

        Returns:
            VectorStoreIndex: The index for the given company, either built from the existing vector store or from the documents.
        """
        try:
            collection = qdrant_client.inner.get_collection(collection_name)
            if collection.status != CollectionStatus.GREEN:
                qdrant_client.inner.delete_collection(collection_name)
                raise Exception(f"Collection {collection_name} not found")

            return VectorStoreIndex.from_vector_store(
                vector_store=qdrant_client.vector_store,
                service_context=qdrant_client.service_context,
                storage_context=qdrant_client.storage_context,
            )
        except Exception:
            return VectorStoreIndex.from_documents(
                company_documents,
                service_context=qdrant_client.service_context,
                storage_context=qdrant_client.storage_context,
            )

    def query(self, query: str):
        """
        Queries the earnings calls data.

        Args:
            query (str): The query to run.

        Returns:
            The query results.
        """
        if self.engine is None:
            raise ValueError("Engine not built yet. Please call build_engine() first.")

        return self.engine.query(query)
