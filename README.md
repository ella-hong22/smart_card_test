# Smart Card Manager: 혁신적인 명함 관리 및 AI 테스트 플랫폼

## 프로젝트 소개
**Smart Card Manager**는 멀티모달 AI 기술을 활용해 명함 이미지를 처리하고, 인맥 정보를 스마트하게 관리하며, 다양한 AI 모델의 성능을 비교·평가할 수 있는 차세대 솔루션입니다. 이 프로젝트는 Google Gemini 및 Ollama API를 통해 이미지와 텍스트 데이터를 분석하고, 사용자 친화적인 대화형 인터페이스로 명함 정보를 추출·정리하며, 결과를 CSV로 저장해 성능을 객관적으로 평가합니다. 

---

## 주요 특징
- **스마트 명함 관리**: 명함 이미지 업로드 후 이름, 전화번호, 회사 등 정보를 자동 추출하고, 만남 맥락(장소, 대화 내용 등)을 추가해 인맥을 체계적으로 관리.
- **멀티모달 AI 테스트**: Google Gemini 및 Ollama를 통해 이미지와 텍스트를 처리, 모델별 응답 속도와 정확도를 비교.
- **사용자 친화적 UI**: Streamlit으로 제작된 대화형 채팅 인터페이스, 드래그앤드롭 및 이모지 기반 이미지 업로드 지원.
- **유연한 확장성**: 새로운 AI 모델 추가 및 사용자 맞춤화 가능.

---

## 설치 및 실행 방법

### 1. 요구사항
- Python 3.8 이상
- Docker (옵션, Ollama 모델 실행 시 필요)
- 필요한 Python 패키지는 `requirements.txt`를 참조하세요.

### 2. 설치
1. 레포지토리를 클론합니다:
    ```bash
    git clone https://github.com/ella-hong22/smart_card_test.git
    cd smart_card_test
    ```

2. 필요한 Python 패키지를 설치합니다:
    ```bash
    pip install -r requirements.txt
    pip install flash-attn --no-build-isolation 별도 설치 필요
    ```

3. `.env` 파일 생성 및 설정:
    프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음과 같이 설정합니다:
    ```
    GOOGLE_API_KEY=your_google_gemini_api_key
    HOST_URL=http://your-ollama-api-endpoint  # Ollama 사용 시
    ```

### 3. 데이터 준비
- `data/images/` 폴더에 테스트할 명함 이미지 파일을 추가합니다 (여러 개 가능).
- `data/questions.txt` 파일에 테스트할 질문을 한 줄씩 작성합니다 (예: "오늘 세미나에서 받은 명함인데, 저장해줄래? | 세미나 분위기 좋았고, 데이터 분석 얘기했어. | 좋아, 다 맞아. 저장해줘.").

### 4. 실행
1. **Streamlit 인터페이스 실행** (명함 관리 및 AI 테스트):
    ```bash
    streamlit run streamlit/app.py
    ```
    - 브라우저에서 열리는 UI로 명함 이미지 업로드 및 대화 가능.

2. **Ollama 모델 테스트 실행** (선택):
    ```bash
    python inference_ollama_models.py  # Ollama 기반 모델 테스트
    python inference_qwen_models.py   # Qwen 모델 테스트
    ```
    - 결과는 `qwen_inference_results.csv`와 같은 CSV 파일로 저장.

---

## 주요 파일 및 폴더 구조
```
smart_card_test/
│
├── data/
│   ├── images/          # 명함 및 테스트용 이미지 저장 폴더
│   └── questions.txt    # 테스트 및 대화용 질문 파일
│
├── streamlit/           # Streamlit 기반 웹 인터페이스
│   └── app.py          # 스마트 명함 관리 웹 애플리케이션
│
├── .env                 # 환경 변수 설정 파일 (API 키 등)
├── .gitignore           # Git 무시 파일
├── inference_ollama_models.py  # Ollama 모델 추론 스크립트
├── inference_qwen_models.py    # Qwen 모델 추론 스크립트
├── ollama_how_to_use.ipynb     # Ollama API 사용 가이드 노트북
├── ollama_model_download.py    # Ollama 모델 다운로드 스크립트
├── qwen_inference_results.csv  # Qwen 모델 테스트 결과
├── README.md             # 이 프로젝트 설명 문서
└── requirements.txt      # Python 의존성 목록
```

---

## 기여 및 피드백
이 프로젝트는 오픈소스로서, 더 나은 명함 관리와 AI 테스트를 위해 기여를 환영합니다. 이슈나 개선 제안을 `GitHub Issues`에 남겨주세요!
