from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

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
    # We ignore the actual image for now and return a demo result.
    # Shape matches what the frontend expects.
    demo = {
        "constellation": "Orion (demo)",
        "lines": [
            [0.20, 0.20, 0.60, 0.30],
            [0.60, 0.30, 0.70, 0.70],
            [0.70, 0.70, 0.20, 0.20],
        ],
        "points": [
            {"x": 0.20, "y": 0.20, "name": "Star A"},
            {"x": 0.60, "y": 0.30, "name": "Star B"},
            {"x": 0.70, "y": 0.70, "name": "Star C"},
        ],
    }
    return JSONResponse({"constellation": "Orion (demo)"})
@app.get("/")
def read_root():
    return {"message": "NightGuide API is running 🚀"}

