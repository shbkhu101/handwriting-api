import io
from PIL import Image
import easyocr
import numpy as np

class HandwritingOCRModel:
    def __init__(self):
        # 모델 로드: 한국어('ko')와 영어('en') 동시 지원 모델 메모리에 탑재
        print("Loading EasyOCR Model (This may take a while)...")
        # GPU 리소스가 없다면 gpu=False로 자동 구동됩니다.
        self.reader = easyocr.Reader(['ko', 'en'], gpu=False)
        print("EasyOCR Model loaded successfully.")

    def predict(self, image_bytes: bytes) -> str:
        try:
            # 1. 파일에서 이미지를 열고 NumPy 배열 형태로 변환 (EasyOCR 요구사항)
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            img_numpy = np.array(image)
            
            # 2. 이미지 배열을 EasyOCR에 넣고 글자 추출!
            result = self.reader.readtext(img_numpy)
            
            # 3. 반환된 텍스트의 언어를 식별하여 (텍스트, 언어) 형태로 가공하기
            processed_results = []
            for bbox, text, conf in result:
                # 간단한 규칙 기반 언어 판별
                has_korean = any(ord('가') <= ord(char) <= ord('힣') for char in text)
                has_english = any('a' <= char.lower() <= 'z' for char in text)
                
                if has_korean and has_english:
                    lang_label = "혼용"
                elif has_korean:
                    lang_label = "한국어"
                elif has_english:
                    lang_label = "영어"
                elif any(char.isdigit() for char in text):
                    lang_label = "숫자"
                else:
                    lang_label = "기호/기타"
                    
                processed_results.append(f"({text}, {lang_label})")
            
            # 최종 결과물 결합
            extracted_text = " ".join(processed_results)
            
            return extracted_text

        except Exception as e:
            raise Exception(f"Failed to process image: {str(e)}")
