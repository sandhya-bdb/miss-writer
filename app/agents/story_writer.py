from langchain_openai import ChatOpenAI

def write_story(themes: list[str], emotions: list[str], core_ideas: list[str]) -> str:
    """
    Generates a creative narrative from structured thoughts using llm.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    
    themes_str = ", ".join(themes)
    emotions_str = ", ".join(emotions)
    ideas_str = "\n".join(f"- {idea}" for idea in core_ideas)
    
    prompt = f"""You are a master storyteller. 
    Turn the following structured thoughts into a coherent, highly creative, and beautiful story.
    Preserve the emotional tone and fill in small narrative gaps smoothly to make it natural.
    
    Themes: {themes_str}
    Emotions: {emotions_str}
    
    Core Ideas:
    {ideas_str}
    
    Write the final story:
    """
    
    response = llm.invoke(prompt)
    return response.content
