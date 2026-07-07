from langchain.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from pathlib import Path
from tools.file_tools import check_file

@tool('keywords_extractor')
def extract_keywords(job_description:str) -> str:
    """Extract important keywords from the provided job description. Identifies required skills, technologies, qualifications, and responsibilities that are critical for the role.
    
    Args: 
        job_description: The full text of the job description.
    Returns:
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

@tool('resume_comparison_score')
def score_resumes(keywords:str, resume_path:str) -> str:
    """Scores and compare all resumes in the resumes folder against the extracted job keywords. Reads each resume, evaluates how well it matches the required skills and qualifications, and returns the name and content of the bst matching resume
    
    Args:
        keywords: The extracted keywords from the job description.
        resume_path: The path to the folder containing the resumes.
    Returns:
        The name and content of the best matching resume as a string.
    """
    resume_folder = Path('inputs/resumes')
    resume_content = ""
    
    for file in resume_folder.glob('*.docx'):
        content = check_file(file)
        resume_content += f"Resume: {file.name}\n{content}\n\n"
        
    messages = [
        SystemMessage(content="You are an expert career coach and resume analyst. Evaluate resumes against job requirements and identify the strongest match concisely."),
        HumanMessage(content=f"Evaluate these resumes against the job keywords and return: 1. Score for each resume (X/10) 2. Name of the winning resume 3. Brief reason why it won (2-3 senteces max) 4. Short bullet list of suggested changes to the winning resume Job Keywords: {keywords} Resumes: {resume_content} Keep the response concise and actionable.")
    ]
    
    model = ChatAnthropic(
        model = 'claude-sonnet-4-6',
        temperature=0,
    )
    
    res = model.invoke(messages)
    
    return res.content