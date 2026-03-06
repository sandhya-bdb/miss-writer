from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import shutil
import logging
from app.graph import build_graph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Miss Writer API", description="Converts spoken thoughts to a creative story.")

graph = build_graph()

class StoryResponse(BaseModel):
    transcript: str
    themes: list[str]
    emotions: list[str]
    core_ideas: list[str]
    story: str

@app.post("/process-audio", response_model=StoryResponse)
async def process_audio(audio: UploadFile = File(...)):
    """
    Upload an audio file, transcribes it, structures the thoughts, and writes a story.
    """
    if not audio.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
        
    file_path = f"/tmp/{audio.filename}"
    try:
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
            
        logger.info(f"Saved audio file to {file_path}")
            
        # Run graph
        initial_state = {"audio_path": file_path}
        result = graph.invoke(initial_state)
        
        return StoryResponse(
            transcript=result.get("transcript", ""),
            themes=result.get("themes", []),
            emotions=result.get("emotions", []),
            core_ideas=result.get("core_ideas", []),
            story=result.get("story", "")
        )
    except Exception as e:
        logger.error(f"Error processing audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Cleaned up audio file: {file_path}")
