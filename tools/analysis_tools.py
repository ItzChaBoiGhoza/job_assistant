from langchain.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

@tool('keywords_extractor')
def extract_keywords(job_description:str) -> str:
    """Extract important keywords from the provided job description. Identifies required skills, technologies, qualifications, and responsibilities that are critical for the role.
    
    Args: 
        job_description: The full text of the job description.
    Return:
        A string of extracted keywords and key phrases.
    """
    messages = [
        SystemMessage(content='You are an expert at analyzing job description. Extract all important keywords including required skills, technologies, qualifications, and responsibilities. Present them in a clear organized list.'),
        HumanMessage(content=f'Extract the keywords from this job description: {job_description}')
    ]
    
    model = ChatAnthropic(
        model = 'claude-sonnet-4-6',
        temperature=0,
    )
    
    res = model.invoke(messages)

    return res.content