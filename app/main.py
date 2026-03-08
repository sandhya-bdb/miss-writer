from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import os
import shutil
import logging
from app.graph import build_graph
from app.database import init_db, save_story, get_all_stories

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Miss Writer API", description="Converts spoken thoughts to a creative story.")

# Initialize the database when the app starts
@app.on_event("startup")
def startup_event():
    init_db()

graph = build_graph()

class StoryResponse(BaseModel):
    transcript: str
    themes: list[str]
    emotions: list[str]
    core_ideas: list[str]
    story: str

@app.post("/process-audio", response_model=StoryResponse)
async def process_audio(
    audio: UploadFile = File(...),
    genre: str = Form("Creative Narrative"),
    tone: str = Form("Engaging"),
    previous_story: str = Form(None)
):
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
        initial_state = {
            "audio_path": file_path,
            "genre": genre,
            "tone": tone,
            "previous_story": previous_story
        }
        result = graph.invoke(initial_state)
        
        # Save the structured outputs and the final story into the database
        save_story(
            genre=genre,
            tone=tone,
            transcript=result.get("transcript", ""),
            themes=result.get("themes", []),
            emotions=result.get("emotions", []),
            core_ideas=result.get("core_ideas", []),
            story=result.get("story", "")
        )
        
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

@app.get("/stories")
async def get_stories():
    """Fetch all saved stories."""
    try:
        stories = get_all_stories()
        return {"stories": stories}
    except Exception as e:
        logger.error(f"Error fetching stories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

