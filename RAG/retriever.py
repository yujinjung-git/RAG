import os
import time
from langchain_community.document_loaders import PyPDFLoader
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

class Retriever:
    def __init__(self, embedding_model='jhgan/ko-sbert-nli'):
        # Initialize embeddings
        self.ko_embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            encode_kwargs={'normalize_embeddings': True, 'batch_size': 16}
        )

        # Initialize text splitters
        self.child_splitter = RecursiveCharacterTextSplitter(chunk_size=300)
        self.parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)

        # Initialize vector stores
        self.vectorstore = Chroma(
            collection_name="full_documents",
            embedding_function=self.ko_embeddings
        )
        self.parentstore = Chroma(
            collection_name="splits_parents",
            embedding_function=self.ko_embeddings
        )
        self.store = InMemoryStore()

        # Initialize retriever
        self.retriever = ParentDocumentRetriever(
            vectorstore=self.parentstore,
            docstore=self.store,
            child_splitter=self.child_splitter,
            parent_splitter=self.parent_splitter,
        )

    def load_pdfs(self, file_paths):
        docs = []
        for file_path in file_paths:
            if not file_path.lower().endswith('.pdf'):
                raise ValueError(f"유효하지 않은 파일 확장자: {file_path}. PDF 파일만 지원됩니다.")
            print(f"PDF 로딩 중: {file_path}")
            start_time = time.time()
            loader = PyPDFLoader(file_path)
            docs.extend(loader.load_and_split())
            print(f"PDF 로딩 완료: {file_path} in {time.time() - start_time} seconds")
        self.retriever.add_documents(docs, ids=None)
        print("PDF 파일이 성공적으로 추가되었습니다.")