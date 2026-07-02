from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
output_dir = os.getenv('OUTPUT_DIR', "~/job_applications")
path = Path(output_dir).expanduser().resolve()
