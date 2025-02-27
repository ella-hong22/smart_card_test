import os
import csv
import time
import torch
from PIL import Image
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor

# 테스트할 모델 리스트
MODELS_TO_TEST = {
    "qwen": [
        # "Qwen/Qwen2.5-VL-3B-Instruct",
        # "Qwen/Qwen2.5-VL-7B-Instruct",
        "Qwen/Qwen2.5-VL-72B-Instruct"
    ]
}

# 시스템 지침 (기존과 동일)
SYSTEM_INSTRUCTION = """
당신은 스마트 명함 관리 서비스를 위한 AI 어시스턴트입니다. 주요 기능은 명함 이미지를 처리하고, 인맥 만남에 대한 맥락 정보를 수집하며, 연락처 정보를 관리하는 것입니다. 다음 지침을 따르세요:
1. 시스템 정의:
   텍스트나 이미지 데이터 형태의 사용자 입력을 받습니다. 응답은 친근하고 대화체여야 하며, 항상 새로운 정보를 처리하거나 다음 단계로 넘어갈 준비가 되어 있어야 합니다.
2. 이미지 처리:
   명함 이미지를 받으면 정보를 분석하고, 다음 세부 정보를 JSON 형식으로 추출하세요:
   <extracted_info>
   {
     "name": "",
     "position": "",
     "company": "",
     "phone": "",
     "email": "",
     "address": "",
     "website": "",
     "other_details": []
   }
   </extracted_info>
3. 맥락 정보 수집:
   이미지 처리 후, 추가 맥락 정보를 수집합니다. 예: "이 사람을 어디서 만났나요?", "무엇을 논의했나요?" 등 친근하게 물어보고, 연락처 정보에 추가합니다.
4. 정보 요약 및 확인:
   추출된 명함 정보와 맥락 정보를 요약해 사용자에게 제시하고 확인을 요청하세요.
5. 상호작용 마무리:
   정보가 정확하면 "이 연락처를 데이터베이스에 추가했습니다. 다른 명함 처리할까요?"로 응답하세요.
친근한 어조를 유지하며, 사용자의 질문이나 설명 요청에 대응하세요。
"""

class QwenModel:
    def __init__(self, checkpoint):
        self.checkpoint = checkpoint
        self.model = None
        self.processor = None
        
    def initialize(self):
        print(f"\n{self.checkpoint} 모델 초기화 중...")
        try:
            self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                self.checkpoint,
                torch_dtype=torch.bfloat16,
                attn_implementation="flash_attention_2",
                device_map="auto"
            )
            self.processor = AutoProcessor.from_pretrained(self.checkpoint)
            print(f"{self.checkpoint} 모델 초기화 완료")
            return True
        except RuntimeError as e:
            if "out of memory" in str(e):
                print(f"GPU 메모리 부족: {self.checkpoint} 모델 스킵")
            else:
                print(f"모델 초기화 실패: {str(e)}")
            return False
            
    def clear(self):
        if self.model is not None:
            del self.model
            del self.processor
            torch.cuda.empty_cache()
            self.model = None
            self.processor = None

def load_data():
    image_files = sorted(os.listdir(os.path.join("data", "images")), 
                         key=lambda x: int(''.join(filter(str.isdigit, x))))
    if not image_files:
        raise FileNotFoundError("이미지 파일을 찾을 수 없습니다.")

    with open(os.path.join("data", "questions.txt"), 'r', encoding='utf-8') as f:
        questions = [line.strip() for line in f if line.strip()]
    if not questions:
        raise FileNotFoundError("질문 파일이 비어있습니다.")

    return image_files, questions

def run_inference(qwen_instance, image_path, conversation_history, is_first_turn=False):
    print(f"\n=== {qwen_instance.checkpoint} 추론 시작 ===")
    if torch.cuda.is_available():
        print(f"GPU 메모리: {torch.cuda.memory_allocated()/1024**3:.2f}GB")
    
    start_time = time.time()
    try:
        messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
        messages.extend(conversation_history)
        print("messages", messages)
        text = qwen_instance.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        
        if is_first_turn:  # 첫 턴: 이미지와 텍스트 처리
            image = Image.open(image_path)
            inputs = qwen_instance.processor(text=[text], images=[image], padding=True, return_tensors="pt")
        else:  # 이후 턴: 텍스트만 처리
            inputs = qwen_instance.processor(text=[text], images=None, padding=True, return_tensors="pt")
        
        inputs = inputs.to('cuda' if torch.cuda.is_available() else 'cpu')
        output_ids = qwen_instance.model.generate(**inputs, max_new_tokens=2000)
        generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, output_ids)]
        response_text = qwen_instance.processor.batch_decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)[0]
        
        inference_time = round(time.time() - start_time, 2)
        input_tokens = len(inputs.input_ids[0])
        output_tokens = len(generated_ids[0])
        print(f"추론 시간: {inference_time}초 / 입력 토큰: {input_tokens} / 출력 토큰: {output_tokens}")
        
        return response_text, inference_time, input_tokens, output_tokens
    except RuntimeError as e:
        if "out of memory" in str(e):
            print("GPU 메모리 부족으로 추론 실패")
            return None, None, None, None
        raise

def run_tests():
    results = []
    try:
        image_files, questions = load_data()
    except FileNotFoundError as e:
        print(f"데이터 로드 실패: {str(e)}")
        return

    for checkpoint in MODELS_TO_TEST['qwen']:
        qwen_instance = QwenModel(checkpoint)
        if not qwen_instance.initialize():
            continue

        for image_path, question_line in zip(image_files, questions):
            turns = question_line.split('|')
            if len(turns) != 3:
                print(f"잘못된 질문 형식: {question_line}")
                continue

            full_image_path = os.path.join('data', 'images', image_path)
            print(f"\n모델: {checkpoint} / 이미지: {os.path.basename(image_path)}")
            
            conversation_history = []
            for turn_idx, turn_question in enumerate(turns, 1):
                print(f"턴 {turn_idx}: {turn_question}")
                if turn_idx == 1:  # 첫 턴: 이미지 포함
                    conversation_history.append({"role": "user", "content": [
                        {"type": "text", "text": turn_question},
                        {"image": full_image_path},
                    ]})
                    response_text, inference_time, input_tokens, output_tokens = run_inference(
                        qwen_instance, full_image_path, conversation_history, is_first_turn=True
                    )
                else:  # 이후 턴: 텍스트만
                    conversation_history.append({"role": "user", "content": [
                        {"type": "text", "text": turn_question}
                    ]})
                    response_text, inference_time, input_tokens, output_tokens = run_inference(
                        qwen_instance, full_image_path, conversation_history, is_first_turn=False
                    )
                
                if response_text is None:  # GPU 메모리 부족
                    break
                
                conversation_history.append({"role": "assistant", "content": response_text})
                
                results.append({
                    "model": checkpoint,
                    "image": os.path.basename(image_path),
                    "turn": turn_idx,
                    "question": turn_question,
                    "response": response_text,
                    "inference_time": inference_time,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens
                })

        qwen_instance.clear()

    if results:
        with open("qwen_inference_results_72b.csv", mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "model", "image", "turn", "question", "response", 
                "inference_time", "input_tokens", "output_tokens"
            ])
            writer.writeheader()
            writer.writerows(results)
        print("\n테스트 결과가 저장되었습니다.")

if __name__ == '__main__':
    run_tests()