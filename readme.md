# PDFQA : RAG-Based Chatbot Prototype

PDFQA는 PDF 문서에서 정보를 검색하고 질문에 답변하는 Python 기반의 시스템입니다. 이 프로그램은 Google Generative AI와 LangChain을 사용해 구현했습니다.

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

### 터미널 사용

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

### IDE 사용 (PyCharm - MacOS)

1. PyCharm을 열고, `Open` 옵션을 선택하여 클론한 프로젝트 폴더를 엽니다.

2. PyCharm에서 가상환경을 설정합니다:
    - `PyCharm` -> `Settings` -> `Project: RAG` -> `Python Interpreter`로 이동합니다.
    - `Add Interpreter` 버튼을 클릭하고 `Existing environment`를 선택합니다.
    - 가상환경의 Python 해석기 경로를 설정합니다 (예: `<프로젝트 경로>/venv/bin/python` 또는 Windows의 경우 `venv\Scripts\python.exe`).
    - `OK`를 클릭하여 설정을 저장합니다.

3. `Run` -> `Edit Configurations...`로 이동합니다.
4. `Script path`에 `main.py` 경로를 설정합니다.
5. `Parameters`에 `--api_key "YOUR_GOOGLE_API_KEY"`를 추가합니다.
6. `Apply`를 클릭하고 `OK`를 클릭합니다.
7. `Run` -> `Run 'main'`을 선택하여 프로그램을 실행합니다.
8. 실행 후, 터미널 창에서 추가할 PDF 파일의 경로를 입력합니다.
9. 명령어를 입력하여 프로그램을 사용합니다:
    - 질문: PDF 파일에서 정보를 검색하여 답변합니다.
    - 추가: 새로운 PDF 파일을 추가합니다.
    - 기록: 현재 대화 히스토리를 출력합니다.
    - exit: 프로그램을 종료합니다.


## 프로그램 구조

```plaintext
RAG
|-- main.py
|-- RAG/
    |-- __init__.py
    |-- qa_system.py
    |-- retriever.py
|-- README.md
|-- requirements.txt