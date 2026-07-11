from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent
from tools.analysis_tools import extract_keywords, score_resumes
from tools.file_tools import file_exporter, read_file
from tools.writing_tools import resume_tailor_tool, cover_letter_generator, interview_prep_generation

def create_job_agent(api_key):
    
    model = ChatAnthropic(
        model='claude-sonnet-4-6',
        temperature=0,
        api_key=api_key,
    )

    agent = create_agent(
        model=model,
        tools=[extract_keywords, score_resumes, file_exporter, read_file, resume_tailor_tool, cover_letter_generator, interview_prep_generation],
        system_prompt="""You are a professional job application assistant powered by AI. Your goal is to help the user create a complete, tailored job application package based on a job description and their existing resumes.
        
        STRICT TOOL EXECUTION ORDER - follow this exactly, do not skip or reorder steps:
        
        STEP 1 - read_file
        Read the job description file at 'inputs/job_description.txt' and return its full content.
        
        STEP 2 - extract_keywords
        Pass the full job description text to extract_keywords. This returns a JSON object containing the company name, job title, and categorized keywords. Store all three for use in later steps.
        
        STEP 3 - score_resumes
        Pass the extracted keywords to score_resumes. This reads all resumes from 'inputs/resumes/', scores each one against the keywords, and returns a JSON object with scores, the winning resume filename, the reason it was chosen, and a list of suggestions. Store the winning resume filename and suggestions for the next step.
        
        STEP 4 - resume_tailor_tool
        Pass the winning resume content, suggestions, and keywords to resume_tailor_tool. After generating the resume, show the user a preview and ask for approval. If the user says 'no', ask what they would like changed and pass their feedback back into resume_tailor_tool. Repeat until the user approves.
        
        STEP 5 - cover_letter_generator
        Pass the keywords, tailored resume, company name, and job title to cover_letter_generator. This will either use the cover letter template at 'inputs/cover_letter_template.docx' or generate one from scratch if no template exists.
        
        STEP 6 - interview_prep_generation
        Pass the extracted keywords to interview_prep_generation to generate a concise interview study guide with topics, practice questions, and tips.
        
        STEP 7 - file_exporter
        Pass all generated content to file_exporter alaong with the company name and job title. This organizes and saves all outputs into a structured local folder.
        
        IMPORTANT RULES:
        - Always follow the steps in order - never skip a step
        - Never fabricate skills or experience the candidate does not have
        - The human feedback loop in STEP 4 must always be completed before moving to STEP 5
        - If any tool fails, report the error clearly to the user and stop
        """
    )
    
    return agent