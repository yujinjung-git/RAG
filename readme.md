# PDFQA 시스템

PDFQA는 PDF 문서에서 정보를 검색하고 질문에 답변하는 Python 기반의 시스템입니다. 이 프로그램은 Google Generative AI와 LangChain을 사용하여 구현되었습니다.

## 주요 기능

- PDF 파일을 로드하여 텍스트를 추출하고 저장
- 질문에 대해 PDF 파일에서 답변을 검색
- 대화형 질문 및 답변 히스토리 저장 및 출력

## 설치 방법

1. 이 리포지토리를 클론합니다.

    ```bash
    git clone https://github.com/yujinjung-git/RAG
    cd RAG
    ```

2. 가상환경을 생성하고 활성화합니다.

    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows의 경우 `venv\Scripts\activate`
    ```

3. 필요한 패키지를 설치합니다.

    ```bash
    pip install -r requirements.txt
    ```

## 사용 방법

1. 프로그램을 실행할 때 Google API 키를 명령줄 인수로 전달합니다.

    ```bash
    python main.py --api_key "YOUR_GOOGLE_API_KEY"
    ```

2. 실행 후, 추가할 PDF 파일의 경로를 입력합니다.

3. 명령어를 입력하여 프로그램을 사용합니다:
    - 질문: PDF 파일에서 정보를 검색하여 답변합니다.
    - 추가: 새로운 PDF 파일을 추가합니다.
    - 기록: 현재 대화 히스토리를 출력합니다.
    - exit: 프로그램을 종료합니다.

## 프로그램 구조

```plaintext
+-----------------------------------------------------+
|                      PDFQA                          |
+-----------------------------------------------------+
| __init__(google_api_key, model_name, embedding_model)|
| - ChatGoogleGenerativeAI                             |
| - HuggingFaceEmbeddings                              |
| - RecursiveCharacterTextSplitter                     |
| - Chroma                                             |
| - InMemoryStore                                      |
| - ParentDocumentRetriever                            |
| - ConversationBufferMemory                           |
| - ConversationalRetrievalChain                       |
|                                                     |
| Methods:                                            |
| - load_pdfs(file_paths)                              |
| - initialize_qa()                                    |
| - ask_question(question)                             |
| - add_pdfs()                                         |
| - print_chat_history()                                |
| - run()                                              |
+-----------------------------------------------------+

