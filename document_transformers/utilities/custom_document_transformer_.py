import os
from typing import Any, Dict, List, Sequence, Type, Union, Optional
from pydantic import BaseModel
from langchain_core.documents import Document
from langchain_core.documents.transformers import BaseDocumentTransformer

from langchain_text_splitters import (CharacterTextSplitter,
                                      RecursiveCharacterTextSplitter,
                                      TokenTextSplitter)

from bson import ObjectId
from pymongo import MongoClient

# MongoDB connection configuration
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING', 'localhost')
client = MongoClient(MONGO_CONNECTION_STRING)
document_store_db_name = "document_store"


class TransformerConfig(BaseModel):
    """Configuration for a transformer, including the transformer type, arguments, and ID modification settings."""
    transformer: Type[BaseDocumentTransformer]
    kwargs: Dict[str, Any] = {}
    add_prefix_to_id: Union[str, None] = None
    add_suffix_to_id: Union[str, None] = None
    add_split_index_to_id: bool = False
    # TODO:
    #  - implement the capabilities to update transformed docs metadata with extra values content in
    #  'add_metadata_to_docs' variable (implement in TransformerMap class)
    add_metadata_to_docs: Dict[str, Any] = None
    output_store: Optional[Dict[str, Any]] = None  # New attribute for output store configuration


class TransformerMapConfig(BaseModel):
    """Configuration for a transformer, including the transformer type, arguments, and ID modification settings."""
    transformer_map: Union[Dict[str, TransformerConfig], None] = None
    default_transformer: Union[Type[BaseDocumentTransformer], None] = None
    default_kwargs: Union[str, None] = None
    # TODO:
    #  - implement the capabilities to applied 'default_add_prefix_to_id', 'default_add_suffix_to_id' and
    #  'default_add_split_index_to_id' effects to transformed (with default options) docs
    #  (implement in TransformerMap class)
    default_add_prefix_to_id: Union[str, None] = None
    default_add_suffix_to_id: Union[str, None] = None
    default_add_split_index_to_id: bool = False
    # TODO:
    #  - implement the capabilities to update transformed (with default options) docs metadata with extra values content
    #  in 'default_add_metadata_to_docs' variable (implement in TransformerMap class)
    default_add_metadata_to_docs: Dict[str, Any] = None
    default_output_store: Optional[Dict[str, Any]] = None  # New attribute for output store configuration


class DocumentTransformerMap(BaseDocumentTransformer):
    """
    Custom transformer for documents that applies specific transformations based on metadata.

    This class allows the dynamic application of different transformers to documents based on
    their metadata, supporting complex matching conditions and default transformations.
    """
    def __init__(self,
                 transformer_map: Dict[str, TransformerConfig],
                 default_transformer: Type[BaseDocumentTransformer] = None,
                 default_kwargs: Dict[str, Any] = None,
                 default_add_prefix_to_id: Union[str, None] = None,
                 default_add_suffix_to_id: Union[str, None] = None,
                 default_add_split_index_to_id: bool = False,
                 default_add_metadata_to_docs: Dict[str, Any] = None,
                 default_output_store: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the CustomDocumentTransformer with the specified parameters.

        Args:
            transformer_map (Dict[str, TransformerConfig]): Mapping of metadata conditions to TransformerConfig.
            default_transformer (Type[BaseDocumentTransformer], optional): Default transformer to use if no specific condition is met.
            default_kwargs (Dict[str, Any], optional): Default kwargs for the default transformer.
        """
        self.transformer_map = transformer_map

        self.default_transformer = default_transformer

        self.default_kwargs = default_kwargs or {}

    def transform_documents(self, documents: Sequence[Document], **kwargs: Any) -> Sequence[Document]:
        """
        Transform a list of documents based on metadata conditions.

        Args:
            documents (Sequence[Document]): A sequence of Documents to be transformed.

        Returns:
            Sequence[Document]: A list of transformed Documents.
        """
        transformed_documents = []
        for doc in documents:
            transformed_doc = self.apply_transformers(doc)
            transformed_documents.extend(transformed_doc)
        return transformed_documents

    def apply_transformers(self, document: Document) -> List[Document]:
        """
        Apply the appropriate transformers to the document based on its metadata.

        Args:
            document (Document): A single document to transform.

        Returns:
            List[Document]: A list of transformed documents.
        """
        matched_transformers = self.match_transformers(document.metadata)
        transformed_docs = [document]

        for transformer_config in matched_transformers:
            transformer_instance = transformer_config.transformer(**transformer_config.kwargs)
            new_transformed_docs = []
            for doc in transformed_docs:
                result_docs = transformer_instance.transform_documents([doc])
                for i, result_doc in enumerate(result_docs):
                    result_doc.metadata["source_document_metadata"] = self.serialize_metadata(doc.metadata)
                    result_doc.metadata["split_index"] = i
                    result_doc.metadata["max_split_index"] = len(result_docs) - 1
                    result_doc.metadata["transformer_config"] = {
                        "transformer": transformer_instance.__class__.__name__,
                        "kwargs": transformer_config.kwargs
                    }
                    result_doc.metadata["id"] = self.modify_id(
                        doc.metadata.get("id", ""), transformer_config, i
                    )
                    new_transformed_docs.append(result_doc)
            transformed_docs = new_transformed_docs

        if not matched_transformers and self.default_transformer:
            default_transformer_instance = self.default_transformer(**self.default_kwargs)
            new_transformed_docs = default_transformer_instance.transform_documents(transformed_docs)
            for i, result_doc in enumerate(new_transformed_docs):
                result_doc.metadata["source_document_metadata"] = self.serialize_metadata(document.metadata)
                result_doc.metadata["split_index"] = i
                result_doc.metadata["max_split_index"] = len(new_transformed_docs) - 1
                result_doc.metadata["transformer_config"] = {
                    "transformer": default_transformer_instance.__class__.__name__,
                    "kwargs": self.default_kwargs
                }
                result_doc.metadata["id"] = self.modify_id(
                    document.metadata.get("id", ""), None, i
                )
            transformed_docs = new_transformed_docs

        return transformed_docs

    def match_transformers(self, metadata: Dict[str, Any]) -> List[TransformerConfig]:
        """
        Match the document's metadata to the appropriate transformers.

        Args:
            metadata (Dict[str, Any]): The metadata of the document.

        Returns:
            List[TransformerConfig]: A list of matched transformer configurations.
        """
        matched_transformers = []
        for condition, transformer_config in self.transformer_map.items():
            if self.metadata_matches_condition(metadata, condition):
                matched_transformers.append(transformer_config)
        return matched_transformers

    def metadata_matches_condition(self, metadata: Dict[str, Any], condition: str) -> bool:
        """
        Check if the document's metadata matches the condition.

        Args:
            metadata (Dict[str, Any]): The metadata of the document.
            condition (str): The condition to match in MongoDB-like query syntax.

        Returns:
            bool: True if metadata matches the condition, else False.
        """
        return self.evaluate_mongo_query(metadata, condition)

    def evaluate_mongo_query(self, metadata: Dict[str, Any], query: str) -> bool:
        """
        Evaluate a MongoDB-like query against the metadata.

        Args:
            metadata (Dict[str, Any]): The metadata of the document.
            query (str): The MongoDB-like query string.

        Returns:
            bool: True if metadata matches the query, else False.
        """
        from mongomock import MongoClient as MockMongoClient
        client = MockMongoClient()
        db = client.test
        collection = db.test_collection
        collection.insert_one(self.serialize_metadata(metadata))
        return collection.find_one(eval(query)) is not None

    @staticmethod
    def serialize_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Serialize metadata, converting ObjectId to string if present.

        Args:
            metadata (Dict[str, Any]): The metadata to serialize.

        Returns:
            Dict[str, Any]: The serialized metadata.
        """
        serialized_metadata = {}
        for key, value in metadata.items():
            if isinstance(value, ObjectId):
                serialized_metadata[key] = str(value)
            elif isinstance(value, dict):
                serialized_metadata[key] = DocumentTransformerMap.serialize_metadata(value)
            else:
                serialized_metadata[key] = value
        return serialized_metadata

    @staticmethod
    def modify_id(original_id: str, transformer_config: TransformerConfig, split_index: int) -> str:
        """
        Modify the document ID based on transformer configuration.

        Args:
            original_id (str): The original document ID.
            transformer_config (TransformerConfig): The transformer configuration.
            split_index (int): The index of the split part.

        Returns:
            str: The modified document ID.
        """
        if transformer_config:
            if transformer_config.add_prefix_to_id:
                original_id = f"{transformer_config.add_prefix_to_id}{original_id}"
            if transformer_config.add_suffix_to_id:
                original_id = f"{original_id}{transformer_config.add_suffix_to_id}"
            if transformer_config.add_split_index_to_id:
                original_id = f"{original_id}_{split_index}"
        return original_id


# Example usage
if __name__ == "__main__":
    # Complex query: author is John Doe OR type is report AND (created in 2023 OR department is engineering)
    complex_query = '''
{
    "$or": [
        {"author": "John Doe"},
        {"type": "report"}
    ],
    "$and": [
        {"$or": [
            {"created": 2023},
            {"department": "engineering"}
        ]}
    ]
}
'''

    transformer_map = {
        complex_query: TransformerConfig(
            transformer=CharacterTextSplitter,
            kwargs={"chunk_size": 1, "chunk_overlap": 0, "separator": " "},
            add_prefix_to_id="PREFIX_",
            add_suffix_to_id="_SUFFIX",
            add_split_index_to_id=True
        ),
    }

    default_transformer = CharacterTextSplitter
    default_kwargs = {"chunk_size": 1000, "chunk_overlap": 200}

    transformer = DocumentTransformerMap(transformer_map, default_transformer, default_kwargs)

    documents = [
        Document(page_content="This is a test document by John Doe, created in 2023.", metadata={"id": "abc", "author": "John Doe", "created": 2023}),
        Document(page_content="This is a report document in the engineering department.", metadata={"id": "def", "type": "report", "department": "engineering"}),
        Document(page_content="This is an unclassified document created in 2022.", metadata={"id": "ghi", "category": "general", "created": 2022})
    ]

    transformed_docs = transformer.transform_documents(documents)
    for doc in transformed_docs:
        print(doc.page_content)
        print(doc.metadata)
