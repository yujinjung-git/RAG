# PDFQA : RAG-Based Chatbot Prototype
<br/>


<br/>
PDFQA는 PDF 문서에서 정보를 검색하고 이를 바탕으로 사용자의 질문에 답변하는 Python 기반의 시스템입니다. 이 프로그램은 Google Generative AI와 LangChain을 사용해 구현했습니다.
<br/><br/>PDFQA is a Python based system that retrieves information from PDF documents and answers user questions based on them. The program was implemented using Google Generative AI and LangChain.

<br/>
<br/>
<br/>



## 💡 주요 기능 / Features

- PDF 파일을 로드하여 텍스트를 추출하고 저장
- 질문에 대해 PDF 파일에서 답변을 검색
- 대화형 질문 및 답변 히스토리 저장 및 출력<br/><br/>

- Load PDF files to extract and save text
- Search PDF files for answers to questions
- Save and output a history of interactive questions and answers


<br/>
<br/>
<br/>

## 💿 설치 방법 / Installation


<br/>

1. 이 리포지토리를 클론합니다. <br/>Clone this repository.

    ```bash
    git clone https://github.com/yujinjung-git/RAG
    cd RAG
    ```


2. 가상환경을 생성하고 활성화합니다. <br/>Create and activate virtual environments.
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows의 경우 `venv\Scripts\activate`
   ```


3. 필요한 패키지를 설치합니다. <br/>Install the required packages.

    ```bash
    pip install -r requirements.txt
    ```
   
<br/>
<br/>
<br/>

## 👩🏻‍💻 사용 방법    / How to Start

<br/>

### ☝🏻 터미널 사용 / Use a Terminal

<br/>

1. 프로그램을 실행할 때 Google API 키를 명령줄 인수로 전달합니다. <br/>Forward the Google API key to a command-line argument when you run the program.

    ```bash
    python main.py --api_key "YOUR_GOOGLE_API_KEY"
    ```


2. 실행 후, 추가할 PDF 파일의 경로를 입력합니다. <br/>After running, enter the path of PDF files you want to add.

3. 명령어를 입력하여 프로그램을 사용합니다: <br/>Enter the command to use the program:

- 질문하기: PDF 파일에서 정보를 검색하여 답변합니다.
- '추가': 새로운 PDF 파일을 추가합니다.
- '기록': 현재 대화 히스토리를 출력합니다.
- '종료': 프로그램을 종료합니다.
<br/>
 <br/>

   - Ask questions: answer by searching for information in PDF files.
   - 'Add': Add new PDF files.
   - 'History': Outputs the current conversation history.
   - 'Exit': Exits the program.
   <br/>
   <br/>
   <br/>

### ✌🏻 IDE 사용 (PyCharm - MacOS) / Use an IDE

<br/>

1. PyCharm을 열고, `Open` 옵션을 선택하여 클론한 프로젝트 폴더를 엽니다. <br/> Open PyCharm, select the 'Open' option to open the cloned project folder.
2. PyCharm에서 가상환경을 설정합니다:
    - `PyCharm` -> `Settings` -> `Project: RAG` -> `Python Interpreter`
    - `Add Interpreter` -> `Existing environment`
    - 인터프리터를 선택합니다. <br/>Select the Interpreter. 
      - `<Project Path>/venv/bin/python`
      - Windows - `venv\Scripts\python.exe`
    - `OK`
3. `Run` -> `Edit Configurations...`
4. `Script path`에 `main.py` 경로를 설정합니다. <br/>Set the 'main.py ' path to 'Script path'.
5. `Parameters`에 `--api_key "YOUR_GOOGLE_API_KEY"`를 추가합니다. <br/> Add `--api_key 'YOUR_GOOGLE_API_KEY'` to `Parameters`.
6. `Apply` -> `OK`
7. `Run` -> `Run 'main'`
8. 실행 후, 터미널 창에서 추가할 PDF 파일의 경로를 입력합니다. <br/> After running, in the Terminal window, enter the path to the PDF file you want to add.
9. 명령어를 입력하여 프로그램을 사용합니다: <br/>Enter the command to use the program:
- 질문하기: PDF 파일에서 정보를 검색하여 답변합니다.
- '추가': 새로운 PDF 파일을 추가합니다.
- '기록': 현재 대화 히스토리를 출력합니다.
- '종료': 프로그램을 종료합니다.
<br/>
 <br/>
  - Ask questions: answer by searching for information in PDF files.
  - 'Add': Add new PDF files.
  - 'History': Outputs the current conversation history.
  - 'Exit': Exits the program.
<br/>
<br/>
<br/>


## 📂 레포지토리 구조

```plaintext
RAG
|-- main.py
|-- RAG/
    |-- __init__.py
    |-- qa_system.py
    |-- retriever.py
|-- README.md
|-- requirements.txt
```
---


