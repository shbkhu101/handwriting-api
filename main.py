from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
import logging

from models.ocr_engine import HandwritingOCRModel

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Handwriting Recognition API",
    description="손글씨 이미지를 받아서 텍스트로 변환해주는 MLOps 백엔드 API",
    version="1.0.0"
)

# 서버 시작 시 모델을 메모리에 로드 (Startup Event)
ocr_model = None

@app.on_event("startup")
async def load_model():
    global ocr_model
    logger.info("Initializing ML Model...")
    ocr_model = HandwritingOCRModel()

@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        return HTMLResponse(content="<h1>UI 파일을 찾을 수 없습니다. static/index.html 을 확인하세요.</h1>")

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": ocr_model is not None}

@app.post("/predict")
async def predict_handwriting(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    try:
        # 이미지 데이터 읽기
        image_bytes = await file.read()
        logger.info(f"Received image: {file.filename}, Size: {len(image_bytes)} bytes")
        
        # 모델 추론
        predicted_text = ocr_model.predict(image_bytes)
        
        return JSONResponse(content={
            "filename": file.filename,
            "predicted_text": predicted_text,
            "status": "success"
        })
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal serve error during prediction")

if __name__ == "__main__":
    import uvicorn
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)
