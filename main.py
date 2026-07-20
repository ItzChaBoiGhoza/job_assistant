from dotenv import load_dotenv
from pathlib import Path
import os
import re
import json
import gspread
from tools.file_tools import read_file, check_file, file_exporter
from tools.analysis_tools import extract_keywords, score_resumes
from tools.writing_tools import resume_tailor_tool, cover_letter_generator, interview_prep_generation
from tools.tracker import job_tracker

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
output_dir = os.getenv('OUTPUT_DIR', "~/job_applications")
output_path = Path(output_dir).expanduser().resolve()

def main():
    job_description = read_file.invoke('inputs/job_description.txt')
    extracted_keywords = extract_keywords.invoke(job_description)
    extracted_keywords = re.sub(r'```json|```', '', extracted_keywords).strip()
    resume_scores = score_resumes.invoke({"keywords": extracted_keywords, "resume_path": "inputs/resumes"})
    resume_scores = re.sub(r'```json|```', '', resume_scores).strip()
    
    keywords_data = json.loads(extracted_keywords)
    company_name = keywords_data['company_name']
    job_title = keywords_data['job_title']
    
    scores_data = json.loads(resume_scores)
    winning_resume = scores_data['winning_resume']
    suggestions = scores_data['suggestions']
    
    winning_resume_content = check_file(f'inputs/resumes/{winning_resume}')
    
    feedback = ""
    
    while True:
        tailored_resume = resume_tailor_tool.invoke({"winning_resume": winning_resume_content,  "suggestion": "\n".join(suggestions), "keywords": extracted_keywords, "feedback": feedback})
        
        print("\n--- TAILORED RESUME PREVIEW ---\n")
        print(tailored_resume)
        print("\n--- END OF PREVIEW ---\n")
        
        approval = input('Do you want to export this resume? (yes/no): ')
        
        if approval.lower() == 'yes' or approval.lower() == 'y':
            break
        else:
            feedback = input('What would like to change?')
    
    tailored_cover_letter = cover_letter_generator.invoke({"keywords": extracted_keywords, "tailored_resume": tailored_resume, "company_name": company_name, "job_title": job_title})
    
    interview_prep = interview_prep_generation.invoke(extracted_keywords)
    
    file_exporter.invoke({"tailored_resume": tailored_resume, "tailored_cover_letter": tailored_cover_letter, "job_description": job_description, "company_name": company_name, "job_title": job_title, "interview_prep": interview_prep})

    job_tracker(company_name, job_title)
    
    print('Application entered to Google Sheets!')
    print(f"Application materials saved to: {output_path/company_name/job_title}")
    
if __name__ == '__main__':
    main()