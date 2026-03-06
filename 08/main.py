from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil
from celery.result import AsyncResult

from worker import process_text_to_audio, app as celery_app
from convert import extract_text_from_pdf, convert_text_to_audio

app = FastAPI(title="Async pdf to audio")

@app.post("/convert-async")
async def text_to_audio(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid file")
        
    pdf_path = f"{file.filename}"
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    output_path = f"{file.filename.replace(".pdf", "")}.mp3"
    task = process_text_to_audio.delay(pdf_path, output_path)
    
    return {
        "id":task.id,
        "message": "task accepted"
        }
    
@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    
    if task_result.state == "PENDING":
        return {"status": "Pending", "message": "Waiting for a worker to pick it up..."}
    
    elif task_result.state == 'SUCCESS':
        result_data = task_result.result 
        return {
            "status": "Completed", 
            "message": "Your audiobook is ready!",
            "file": result_data.get("file")
        }
        
    elif task_result.state == 'FAILURE':
        return {"status": "Failed", "error": str(task_result.info)}
        
    else:
        return {"status": task_result.state}
    
@app.get("/download/{filename}")
async def download_audio(filename: str):
    """Allows the user to download the finished file."""
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail="File not found or not ready yet.")
    return FileResponse(filename, media_type="audio/mpeg", filename=filename)