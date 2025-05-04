from typing import Sequence, ClassVar
from langchain.schema import Document
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors.base import BaseDocumentCompressor
from langchain.retrievers.document_compressors import DocumentCompressorPipeline
from langchain_chroma import Chroma
from pydantic.v1 import Extra
from sentence_transformers import CrossEncoder
from config import (
    VECTOR_STORE_DIR, BM25_K, VECTOR_STORE_K, RERANKER_TOP_N,
    ENSEMBLE_WEIGHTS, RERANKER_MODEL, OPENAI_API_KEY
)
from models import embeddings, cross_encoder

class BgeRerank(BaseDocumentCompressor):
    model_name: str = RERANKER_MODEL
    top_n: int = RERANKER_TOP_N
    model: ClassVar[CrossEncoder] = cross_encoder

    def bge_rerank(self, query, docs):
        model_inputs = [[query, doc] for doc in docs]
        scores = self.model.predict(model_inputs)
        results = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        return results[:self.top_n]
    
    class Config:
        extra = Extra.forbid 
        arbitrary_types_allowed = True

    def compress_documents(
            self,
            documents: Sequence[Document],
            query: str,
            callbacks=None,
    ) -> Sequence[Document]:
        if len(documents) == 0:
            return []
        
        doc_list = list(documents)
        _docs = [d.page_content for d in doc_list]
        results = self.bge_rerank(query, _docs)
        final_results = []
        for r in results:
            doc = doc_list[r[0]]
            doc.metadata['relevance_score'] = r[1]
            final_results.append(doc)
        return final_results

def setup_retrievers(split_docs):
    # Инициализация BM25 ретривера
    bm25_retriever = BM25Retriever.from_documents(split_docs)
    bm25_retriever.k = BM25_K

    # embeddings.api_key=OPENAI_API_KEY
    # print("my key:",OPENAI_API_KEY)
    # Инициализация векторного хранилища
    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory=str(VECTOR_STORE_DIR),
        collection_name='testing_documents'
    )

    # Инициализация векторного ретривера
    vs_retriever = vectorstore.as_retriever(search_kwargs={"k": VECTOR_STORE_K})

    # Создание ансамбля ретриверов
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vs_retriever],
        weights=ENSEMBLE_WEIGHTS
    )

    # Настройка реранкера
    reranker = BgeRerank(top_n=RERANKER_TOP_N)

    # Создание пайплайна компрессии
    pipeline_compressor = DocumentCompressorPipeline(
        transformers=[reranker]
    )

    # Создание финального ретривера с компрессией
    compression_pipeline = ContextualCompressionRetriever(
        base_compressor=pipeline_compressor,
        base_retriever=ensemble_retriever
    )

    return compression_pipeline, vectorstore 