import io
import time
from PIL import Image

class HandwritingOCRModel:
    def __init__(self):
        # 모델 로드 (생성자에서 한 번만 호출해서 메모리에 올려둠)
        print("Loading OCR Model...")
        # 실제 모델(easyocr, pytesseract 등)을 초기화하는 로직
        # self.reader = easyocr.Reader(['ko','en'])
        time.sleep(1) # 모델 로딩 시뮬레이션
        print("Model loaded successfully.")

    def predict(self, image_bytes: bytes) -> str:
        """
        이미지 바이트를 입력받아 텍스트를 반환합니다.
        """
        try:
            # 바이트 데이터를 PIL 이미지로 변환
            image = Image.open(io.BytesIO(image_bytes))
            
            # TODO: 여기에 실제 모델 추론 코드 작성
            # ex) result = self.reader.readtext(image)
            # return ' '.join([res[1] for res in result])
            
            # 현재는 Mockup 결과를 반환
            return f"이 텍스트는 이미지(크기: {image.width}x{image.height})에서 추출된 가짜 결과입니다."
        except Exception as e:
            raise Exception(f"Failed to process image: {str(e)}")
