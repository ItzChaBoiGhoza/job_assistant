from langchain.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage

@tool("resume_tailoring")
def tailor_resume(winning_resume:str, suggestion:str, keywords:str) -> str:
    """Tailor the resume from the given suggestions based on the job description.
    
    Args:
        winning_resume: The winning resume from score resume tool.
        suggestion: The suggestions given by the score resume tool.
        keywords: The extracted keywords from the job description.
    Return:
        Returns a string of tailored resume.
    """
    
    message = [
        SystemMessage(content="You are an expert career coach and resume writer. Your task is to tailor a resume to match a specific job description while keeping the content truthful and professional. Preserve the candidate's real experience but reframe, reorder, and enhance wording to better align with the role."),
        HumanMessage(content=f"""Tailor the resume below using the suggestions and job keywords provided.
                     
                     Rules: 
                     - Do not invent experience or skills the candidate does not have
                     - Reorder and reframe existing content to highlight relevance
                     - Use keywords from the job description naturally throughout
                     - Keep the same resume structure and sections
                     - Return only the complete tailored resume, no commentary
                     - Do not add summary section
                     - Keep the length of resume to 1 single page
                     
                     Job Keywords: {keywords}
                     
                     Suggestions: {suggestion}
                     
                     Original Resume: {winning_resume}
                     """)
    ]
    
    model = ChatAnthropic(
        model = 'claude-sonnet-4-6',
        temperature= 0
    )
    
    res = model.invoke(message)
    
    return res.content