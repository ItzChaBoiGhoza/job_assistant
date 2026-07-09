from langchain.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from tools.file_tools import check_file

@tool("resume_tailor_tool")
def resume_tailor_tool(winning_resume:str, suggestion:str, keywords:str) -> str:
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

@tool('cover_letter_generator_tool')
def cover_letter_generator(keywords: str, tailored_resume: str, company_name: str, job_title: str) -> str:
    """Reads the cover letter, and tailor it with the resume and based on the keywords from the job description.
    
    Args:
        keywords: The extracted keywords from the job description.
        tailored_resume: The tailored resume based on extracted keywords from the job description.
        company_name: The extracted company name from the job description.
        job_title: The extracted job title from the job description.
    Return:
        Returns a string of tailored cover letter.
    """
    cover_letter_template = check_file('inputs/cover_letter_template.docx')
    
    if cover_letter_template == "":
        return "Missing cover letter template"
    else:
        model = ChatAnthropic(
            model='claude-sonnet-4-6',
            temperature=0
        )
        
        message = [
            SystemMessage(content='You are an expert career coach and cover letter analyst and writer. Your tasks is to evaluate the cover letter template, and make changes based on the keywords and tailored resume.'),
            HumanMessage(content=f"""Tailor the cover letter using the tailored resume and keywods:
                         
                         Rules:
                         - Do not invent experience or skills the candidate does not have
                         - Use keywords from the job description naturally throughout
                         - Return only the complete tailored cover letter, no commentary
                         - Keep the length of cover letter to 1 single page
                         - Replace the company's name and job title 
                         
                         Cover Letter Template: {cover_letter_template}
                         
                         Job Keywords: {keywords}
                         
                         Tailored Resume: {tailored_resume}
                         
                         Company Name: {company_name}
                         
                         Job Title: {job_title}
                         """)
        ]
        
        res = model.invoke(message)
        
        return res.content
    
@tool('interview_prep_tool')
def interview_prep_generation(keywords:str) -> str:
    """Generates a study guide for interview based on job's description.
    
    Args:
        keywords: The extracted keywords from the job description.
    Return:
        Returns a string of generated study guide
    """
    model = ChatAnthropic(
        model='claude-sonnet-4-6',
        temperature=0
    )
    
    message = [
        SystemMessage(content='You are an expert career coach and ex-manager that does a lot of interviews. Your tasks is to provide a study guide for interview based on the job description, a practice interview questions that might be asked, and tips to prepare or to be ready.'),
        HumanMessage(content=f"""From the extracted keywords from job description come up with a study guide for interview prep. 
                     
                    Rules:
                        - Key topics to study for the interview
                        - Potential interview questions to practice
                        - Tips specific for the role (prepare for interview)
                        
                    Keywords: {keywords}
                        
                    Keep it short and concise. 
                     """)
    ]
    
    res = model.invoke(message)
    
    return res.content