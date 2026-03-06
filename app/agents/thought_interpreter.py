from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List

class StructuredThoughts(BaseModel):
    themes: List[str] = Field(description="Main themes of the thoughts")
    emotions: List[str] = Field(description="Emotions expressed")
    core_ideas: List[str] = Field(description="Organized list of key ideas extracted from fragmented thoughts")

def interpret_thoughts(text: str) -> StructuredThoughts:
    """
    Takes fragmented transcript text and extracts structured thoughts.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    structured_llm = llm.with_structured_output(StructuredThoughts)
    
    prompt = f"""You are an expert thought interpreter. 
    A user has spoken the following fragmented thoughts. 
    Your job is to interpret them, extract themes and emotions, and organize the core ideas into a logical flow.
    
    User's thoughts:
    {text}
    """
    
    # Using invoke, the response will be a StructuredThoughts object
    return structured_llm.invoke(prompt)
