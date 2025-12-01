from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fusion_worker import process_image
from video_processor import analyze_video

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    data = await file.read()
    result = process_image(data)
    return {"status": "ok", "result": result}

@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    data = await file.read()
    try:
        result = analyze_video(data)
        return {"status": "ok", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
