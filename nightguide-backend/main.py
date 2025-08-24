from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from constellation_detector import ConstellationDetector
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="NightGuide API", version="1.0.0")

# Initialize constellation detector (with optional CNN support)
import os
cnn_model_path = os.getenv("CNN_MODEL_PATH")
use_cnn = os.getenv("USE_CNN", "false").lower() == "true"

detector = ConstellationDetector(use_cnn=use_cnn, cnn_model_path=cnn_model_path)

# CORS for local dev (open for hackathon; tighten later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    """Upload and analyze a night sky image for constellation detection"""
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read file content
        content = await file.read()
        
        # Process image
        result = detector.process_image(content)
        
        logger.info(f"Processed image: {file.filename}, detected: {result['constellation']}")
        
        return JSONResponse(result)
        
    except ValueError as e:
        logger.error(f"Image processing error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/")
def read_root():
    return {
        "message": "NightGuide API is running 🚀",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/upload - POST - Upload image for constellation detection",
            "health": "/health - GET - API health check"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "NightGuide API"}

@app.get("/constellations")
def get_constellations():
    """Get list of available constellations"""
    return {
        "constellations": list(detector.constellations.keys()),
        "count": len(detector.constellations)
    }

