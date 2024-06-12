import time

from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

class QASystem:
    def __init__(self, google_api_key, retriever, model_name='gemini-1.5-pro-latest'):
        self.google_api_key = google_api_key
        self.retriever = retriever

        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(model=model_name, api_key=google_api_key)

        # Initialize memory
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key='answer')

        # Initialize QA chain with conversational memory
        self.qa = None

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
        result = self.qa({"question": question, "chat_history": self.memory.chat_memory})
        print(f"질문 처리 완료: {question} in {time.time() - start_time} seconds")
        self.memory.save_context({"question": question}, {"answer": result['answer']})
        return result

    def add_pdfs(self):
        file_paths_input = input("추가할 PDF 파일들의 경로를 콤마(,)로 구분하여 입력하세요: ")
        file_paths = [fp.strip() for fp in file_paths_input.split(',')]
        self.load_pdfs(file_paths)
        self.initialize_qa()

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
