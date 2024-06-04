import os
import time
import argparse
from langchain_community.document_loaders import PyPDFLoader
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import warnings

class PDFQA:
    def __init__(self, google_api_key, model_name='gemini-1.5-pro-latest', embedding_model='jhgan/ko-sbert-nli'):
        self.google_api_key = google_api_key

        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(model=model_name, api_key=google_api_key)  # 여기서 API 키를 전달합니다.

        # Initialize embeddings
        self.ko_embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            encode_kwargs={'normalize_embeddings': True}
        )

        # Initialize text splitters
        self.child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
        self.parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)

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

        # Initialize memory
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key='answer')

        # Initialize QA chain with conversational memory
        self.qa = None

    def load_pdfs(self, file_paths):
        docs = []
        for file_path in file_paths:
            print(f"Loading PDF: {file_path}")
            start_time = time.time()
            loader = PyPDFLoader(file_path)
            docs.extend(loader.load_and_split())
            print(f"Loaded PDF: {file_path} in {time.time() - start_time} seconds")
        self.retriever.add_documents(docs, ids=None)
        print("PDF 파일이 성공적으로 추가되었습니다.")

    def initialize_qa(self):
        print("QA 시스템 초기화 중...")
        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            return_source_documents=True
        )
        print("QA 시스템 초기화 완료")


    def ask_question(self, question):
        if not self.qa:
            raise ValueError("QA 시스템이 초기화되지 않았습니다. 먼저 initialize_qa()를 호출하세요.")
        print(f"질문 처리 중: {question}")
        start_time = time.time()
        result = self.qa({"question": question, "chat_history": self.memory.load_memory_variables({"output_key": "answer"})})
        print(f"질문 처리 완료: {question} in {time.time() - start_time} seconds")
        return result

    def add_pdfs(self):
        file_paths_input = input("추가할 PDF 파일들의 경로를 콤마(,)로 구분하여 입력하세요: ")
        file_paths = [fp.strip() for fp in file_paths_input.split(',')]
        self.load_pdfs(file_paths)

    def print_chat_history(self):
        for i, message in enumerate(self.memory.chat_memory):
            print(f"Message {i + 1}: {message}")

    def run(self):
        while True:
            query = input("\n명령어를 입력하세요 (질문, '추가', '기록', 'exit' 중 선택): ").strip()
            if query.lower() in ['exit', '종료']:
                print("프로그램을 종료합니다.")
                break
            elif query.lower() == '추가':
                self.add_pdfs()
            elif query.lower() == '기록':
                self.print_chat_history()
            else:
                result = self.ask_question(query)
                print("\n응답:", result['answer'])
                for doc in result['source_documents']:
                    print("\n출처 문서:", doc.metadata['source'])
                    print(doc.page_content)

if __name__ == "__main__":
    # OpenMP 경고 무시 설정
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    warnings.filterwarnings("ignore")

    # ArgumentParser를 사용하여 명령줄 인수 처리
    parser = argparse.ArgumentParser(description="PDF QA 시스템")
    parser.add_argument('--api_key', type=str, required=True, help="Google API 키")
    args = parser.parse_args()

    # PDFQA 객체 생성
    pdf_qa = PDFQA(google_api_key=args.api_key)  # args.api_key를 google_api_key로 전달

    # PDF 파일 경로 입력
    file_paths_input = input("PDF 파일들의 경로를 콤마(,)로 구분하여 입력하세요: ")
    file_paths = [fp.strip() for fp in file_paths_input.split(',')]
    pdf_qa.load_pdfs(file_paths)

    # QA 시스템 초기화
    pdf_qa.initialize_qa()

    # 질문 루프 시작
    pdf_qa.run()
