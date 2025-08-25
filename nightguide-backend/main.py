import os
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from starlette.background import BackgroundTask # <-- 1. ADD THIS IMPORT
import shutil
from pipeline import run_full_pipeline

app = FastAPI()
MODEL_PATH = "models/best.pt"
YAML_PATH = "models/data.yaml"
TEMP_DIR = "temp_images"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/upload")
async def upload_and_run_pipeline(file: UploadFile = File(...)):
    unique_id = str(uuid.uuid4())
    input_filename = f"{unique_id}_{file.filename}"
    output_filename = f"{unique_id}_processed.jpg"
    
    input_path = os.path.join(TEMP_DIR, input_filename)
    output_path = os.path.join(TEMP_DIR, output_filename)
    
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    success = run_full_pipeline(
        image_path=input_path,
        model_path=MODEL_PATH,
        yaml_path=YAML_PATH,
        output_path=output_path
    )
    
    os.remove(input_path)
    
    if not success:
        return JSONResponse(status_code=500, content={"error": "Failed to process image or find constellations."})
        
    # --- 2. THIS IS THE CORRECTED RETURN STATEMENT ---
    cleanup_task = BackgroundTask(os.remove, output_path)
    return FileResponse(output_path, media_type="image/jpeg", background=cleanup_task)

@app.get("/health")
def health_check():
    return {"status": "ok"}