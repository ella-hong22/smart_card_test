import os
import requests
from dotenv import load_dotenv
import json
import sys
from time import sleep

# .env 파일에서 환경변수 로드
load_dotenv()
HOST_URL = os.getenv('HOST_URL')
if HOST_URL is None:
    raise ValueError(".env 파일에 HOST_URL이 정의되어 있지 않습니다.")

def create_progress_bar(progress, width=50):
    """프로그레스 바 생성"""
    filled = int(width * progress / 100)
    bar = '█' * filled + '░' * (width - filled)
    return f'[{bar}] {progress:.1f}%'

def download_model(model_name):
    """
    Ollama에서 지정한 모델을 다운로드하는 함수입니다.
    :param model_name: 다운로드할 모델의 이름
    """
    try:
        url = f"{HOST_URL}/api/pull"
        payload = {"model": model_name, "stream": True}
        response = requests.post(url, json=payload, stream=True)
        
        if response.status_code != 200:
            print(f"\n❌ 모델 다운로드 중 오류 발생: {response.status_code}")
            return

        current_status = ""
        
        for line in response.iter_lines():
            if line:
                try:
                    status_data = json.loads(line.decode('utf-8'))
                    
                    # 상태 업데이트
                    if 'status' in status_data:
                        current_status = status_data['status']
                    
                    # 진행률 계산 및 표시
                    if 'total' in status_data and 'completed' in status_data:
                        progress = (status_data['completed'] / status_data['total']) * 100
                        progress_bar = create_progress_bar(progress)
                        
                        # 같은 줄에 업데이트
                        sys.stdout.write(f'\r📥 {model_name}: {progress_bar} | {current_status}')
                        sys.stdout.flush()
                    else:
                        # 진행률 정보가 없는 경우 상태만 표시
                        sys.stdout.write(f'\r📥 {model_name}: {current_status}' + ' ' * 50)
                        sys.stdout.flush()
                        
                except json.JSONDecodeError:
                    continue

        # 다운로드 완료 메시지
        print(f"\n✅ {model_name} 다운로드 완료!")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")

if __name__ == '__main__':
    models = [
        # "bsahane/Qwen2.5-VL-7B-Instruct:Q4_K_M_benxh",
        # "erwan2/DeepSeek-Janus-Pro-7B",
        "llava-llama3",
    ]
    
    for model in models:
        download_model(model)
        sleep(0.5)  # 다음 모델 다운로드 전 잠시 대기