from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from app.services.speech_to_text import transcribe_audio
from app.agents.thought_interpreter import interpret_thoughts
from app.agents.story_writer import write_story
import logging

logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    audio_path: str
    transcript: str
    themes: List[str]
    emotions: List[str]
    core_ideas: List[str]
    story: str
    genre: str
    tone: str
    previous_story: str

def speech_to_text_node(state: AgentState):
    logger.info("Running speech_to_text_node")
    transcript = transcribe_audio(state["audio_path"])
    return {"transcript": transcript}

def thought_interpreter_node(state: AgentState):
    logger.info("Running thought_interpreter_node")
    structured = interpret_thoughts(state["transcript"])
    return {
        "themes": structured.themes,
        "emotions": structured.emotions,
        "core_ideas": structured.core_ideas
    }

def story_writer_node(state: AgentState):
    logger.info("Running story_writer_node")
    story = write_story(
        themes=state["themes"], 
        emotions=state["emotions"], 
        core_ideas=state["core_ideas"],
        genre=state.get("genre", "Creative Narrative"),
        tone=state.get("tone", "Engaging"),
        previous_story=state.get("previous_story", None)
    )
    return {"story": story}

def build_graph():
    """
    Builds the LangGraph reasoning pipeline for the Voice-to-Story Agent.
    """
    workflow = StateGraph(AgentState)
    
    workflow.add_node("speech_to_text", speech_to_text_node)
    workflow.add_node("thought_interpreter", thought_interpreter_node)
    workflow.add_node("story_writer", story_writer_node)
    
    workflow.add_edge(START, "speech_to_text")
    workflow.add_edge("speech_to_text", "thought_interpreter")
    workflow.add_edge("thought_interpreter", "story_writer")
    workflow.add_edge("story_writer", END)
    
    return workflow.compile()
