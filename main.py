import argparse, os
from RAG import QASystem, Retriever, initialize_environment

if __name__ == "__main__":
    initialize_environment()

    # ArgumentParser를 사용하여 명령줄 인수 처리
    parser = argparse.ArgumentParser(description="PDF QA 시스템")
    parser.add_argument('--api_key', type=str, required=True, help="Google API 키")
    args = parser.parse_args()

    # Retriever 객체 생성
    retriever = Retriever()

    while True:
        # PDF 파일 경로 입력
        file_paths_input = input("PDF 파일들의 경로를 콤마(,)로 구분하여 입력하세요: ")
        file_paths = [fp.strip() for fp in file_paths_input.split(',')]

        valid = True
        for file_path in file_paths:
            if not file_path.lower().endswith('.pdf'):
                print(f"지원되지 않는 파일 확장자: {file_path} PDF 파일만 지원됩니다.")
                valid = False
                break
            elif not os.path.exists(file_path):
                print(f"파일이 존재하지 않습니다: {file_path} 유효한 파일 경로를 입력하세요.")
                valid = False
                break

        if valid:
            retriever.load_pdfs(file_paths)
            break


    # QASystem 객체 생성
    qa_system = QASystem(google_api_key=args.api_key, retriever=retriever.retriever)

    # QA 시스템 초기화
    qa_system.initialize_qa()

    # 질문 루프 시작
    qa_system.run()
