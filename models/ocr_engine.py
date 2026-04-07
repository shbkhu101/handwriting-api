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
            
            # 3. 반환된 결과 리스트들을 띄어쓰기로 합쳐서 평문 텍스트로 만들기
            # readtext의 결과물 구조 = [(좌표, 추출된 텍스트, 신뢰도_확률), ...]
            extracted_text = " ".join([text[1] for text in result])
            
            return extracted_text

        except Exception as e:
            raise Exception(f"Failed to process image: {str(e)}")
