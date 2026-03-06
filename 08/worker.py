from celery import Celery
import os
from convert import extract_text_from_pdf, convert_text_to_audio

app = Celery(
    "my-redis",
    broker="redis://localhost:6379/0",
    backend="redis://127.0.0.1:6379/0"
)

@app.task(name="process_audiobook")
def process_text_to_audio(file_path: str, output_path: str):
    print("worker received for {file_path}")
    
    try:
        text = extract_text_from_pdf(file_path)
        convert_text_to_audio(text, output_path)
        
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return {"message":"success",
                "file": output_path}
        
    except Exception as e:
        return {
            "message":"Task failed",
            "error": str(e)
        }