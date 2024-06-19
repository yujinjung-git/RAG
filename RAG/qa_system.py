import time

from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

class QASystem:
    # Google API 키와 리트리버를 인수로 받아 초기화 / Initializes the QASystem with a Google API key and a retriever.
    # Google Generative AI 모델 설정 & 초기화 / Sets up the Google Generative AI model with specified generation configurations.
    # 대화 기록 저장 메모리 초기화 / Initializes a conversation memory buffer.
    # QA체인 초기화 변수 선언 / Prepares a variable to hold the QA chain.
    def __init__(self, google_api_key, retriever, model_name='gemini-1.5-pro-latest'):
        self.google_api_key = google_api_key
        self.retriever = retriever
        self.docs = []

        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(model=model_name, api_key=google_api_key, generation_config=generation_config)


        # Initialize memory
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key='answer')

        # Initialize QA chain with conversational memory
        self.qa = None

    # ConversationalRetrievalChain 생성 후 QA 시스템으로 설정 / Creates and sets up a conversational retrieval chain for the QA system.
    def initialize_qa(self):
        print("QA 시스템 초기화 중...")
        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            return_source_documents=True
        )
        print("QA 시스템 초기화 완료")



    # 사용자의 질문을 처리해 답변 생성 / Processes a user's question and generates an answer.
    # QA시스템이 초기화되지 않은 경우 오류 발생 / Raises an error if the QA system is not initialized.
    # 질문 처리 소요 시간 출력 / Prints the start and end time of question processing.
    # 질문에 대한 답변을 반환하고 대화 기록에 저장 / Returns the answer to the question and saves the conversation context.
    def ask_question(self, question):
        if not self.qa:
            raise ValueError("QA 시스템이 초기화되지 않았습니다. 먼저 initialize_qa()를 호출하세요.")
        print(f"질문 처리 중: {question}")
        start_time = time.time()
        result = self.qa({"question": question, "chat_history": self.memory.chat_memory})
        print(f"질문 처리 완료: {question} in {time.time() - start_time} seconds")
        self.memory.save_context({"question": question}, {"answer": result['answer']})
        return result



    # 파일 경로 참조 후 PDF 파일 로드 & 분할 / Loads and splits PDF files from the given file paths.
    # 확장자 확인, .pdf 아닐 시 오류 발생 / Checks if each file has a .pdf extension, raising an error if not.
    # 각 PDF 파일 로드 & 분할 소요 시간 출력 / Prints the start and completion time for loading each PDF file.
    # 로드된 문서 리트리버에 추가 / Adds the loaded documents to the retriever.
    def load_pdfs(self, file_paths):
        for file_path in file_paths:
            if not file_path.lower().endswith('.pdf'):
                raise ValueError(f"유효하지 않은 파일 확장자: {file_path}. PDF 파일만 지원됩니다.")
            print(f"PDF 로딩 중: {file_path}")
            start_time = time.time()
            loader = PyPDFLoader(file_path)
            self.docs.extend(loader.load_and_split())
            print(f"PDF 로딩 완료: {file_path} in {time.time() - start_time} seconds")
        self.retriever.add_documents(self.docs, ids=None)
        print("PDF 파일이 성공적으로 추가되었습니다.")

    # 추가할 PDF 파일 경로 입력 요청 / Prompts the user to input the paths of PDF files to add.
    # 파일 경로 참조 후 PDF 로드 & 분할 / Loads and splits the specified PDF files.
    # QA시스템 초기화 / Initializes the QA system after adding the PDF files.
    def add_pdfs(self):
        file_paths_input = input("추가할 PDF 파일들의 경로를 콤마(,)로 구분하여 입력하세요: ")
        file_paths = [fp.strip() for fp in file_paths_input.split(',')]
        try:
            self.load_pdfs(file_paths)
        except ValueError as e:
            print(e)
            return
        self.initialize_qa()



    # 대화 기록 출력 / Prints the chat history.
    # 각 메시지의 순서와 내용 출력 / Displays each message in the conversation history.
    def print_chat_history(self):
        for i, message in enumerate(self.memory.chat_memory):
            print(f"Message {i + 1}: {message}")



    # 질문을 입력받아 답변 생성 및 출력 / Accepts a question, generates an answer, and prints it.
    # '종료' 명령어를 통해 프로그램 종료 / Exits the program with the 'Exit' command.
    # '추가' 명령어를 통해 프로그램 수행 중 PDF파일 추가 업로드 / Adds PDF files with the 'Add' command.
    # '기록' 명령어를 통해 대화 기록 출력 / Prints the chat history with the 'History' command.
    def run(self):
        while True:
            query = input("\n명령어를 입력하세요 (질문하기, '추가', '기록', '종료' 중 선택): ").strip()
            if query.lower() in ['종료', 'exit']:
                print("Exit the program.")
                break
            elif query.lower() in ['추가', 'add']:
                self.add_pdfs()
            elif query.lower() in ['기록', 'history']:
                self.print_chat_history()
            else:
                result = self.ask_question(query)
                print("\n응답:", result['answer'])
                '''for doc in result['source_documents']:
                    print("\nsource document:", doc.metadata['source'])
                    print(doc.page_content)'''
