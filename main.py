from dotenv import load_dotenv
from pathlib import Path
import os
from agent import create_job_agent

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
output_dir = os.getenv('OUTPUT_DIR', "~/job_applications")
path = Path(output_dir).expanduser().resolve()

def main():
    
    create_job_agent(api_key)
    print("Agent was created successfully!")
    
if __name__ == '__main__':
    main()