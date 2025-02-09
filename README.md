# Smart Card Test (예시 프로젝트 이름)

## 프로젝트 소개
**Smart Card**는 이미지와 텍스트 데이터를 기반으로 다양한 AI 모델을 테스트하고, 성능을 비교하기 위한 도구입니다.  
이 프로젝트는 Ollama API를 활용하여 이미지 및 텍스트 입력에 대한 모델의 응답을 분석하며, 결과를 CSV 파일로 저장합니다.

---

## 설치 및 실행 방법

### 1. 요구사항
- Python 3.8 이상
- Docker (옵션)
- 필요한 Python 패키지는 `requirements.txt`를 참조하세요.

### 2. 설치
1. 레포지토리를 클론합니다.
    ```bash
    git clone https://github.com/yourusername/smart_card_test.git
    cd smart_card_test
    ```

2. 필요한 Python 패키지를 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```

3. `.env` 파일 생성 및 설정:
    프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음과 같이 설정합니다.
    ```
    HOST_URL=http://your-ollama-api-endpoint
    ```

### 3. 데이터 준비
- `data/images/` 폴더에 테스트할 이미지 파일을 추가합니다.
- `data/questions.txt` 파일에 테스트할 질문을 한 줄씩 작성합니다.

### 4. 실행
1. 모델 테스트 스크립트 실행:
    ```bash
    python test_model.py
    ```

2. 테스트 결과 확인:
    - 실행 결과는 `test_results.csv` 파일에 저장됩니다.

---

## 주요 파일 및 폴더 구조
smart_card_test/
│
├── data/
│   ├── images/          # 테스트용 이미지 저장 폴더
│   └── questions.txt    # 테스트용 질문 파일
│
├── .env                 # 환경 변수 파일
├── model_download.py    # 모델 다운로드 스크립트
├── ollama_how_to_use.ipynb  # Ollama API 예제 
├── requirements.txt     # Python 의존성 목록
├── test_model.py        # 모델 테스트 실행 파일
└── test_results.csv     # 테스트 결과 저장 파일
# smart_card_test
