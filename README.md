# Job Application Assistant

A command-line tool powered by Claude AI to help you with job application process. It reads your resume(s), a job description, and an optional cover letter template, then produces a tailored resume, cover letter, and interview preparation guide. Finally, the tool organize all the output (resume, cover letter, job description, and interview preparation guide) into a local folder ready for submission.

---

## Features

### Resume Scoring
Rates each resume against the job description out of 10, chooses which resume is the best-fitting resume, brief explanation why it was chosen, and provide suggestions for improvement.

### Resume Tailoring
Refines the winning resume based on the scoring suggestions without fabricating skills or experiences you do not have. Includes a feedback loop: review the output, approve it, or describe what you would like changed and the AI will revise it.

### Cover Letter Generation
Uses your cover letter template to produce a tailored cover letter aligned with the job description and your tailored resume. If no template is provided, the AI writes one from scratch.

### Interview Prep Guide
Generates a study guide based on the job description, including key topics to study, practice interview questions, and interview tips.

---

## Requirements
- Python
- pip
- Anthropic API key

---

## Setup

1. **Clone the Repository**
    ```bash
    git clone https://github.com/ItzChaBoiGhoza/job_assistant.git
    cd job_assistant
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure environment**
    ```bash
    cp .env_example .env
    ```
    open `.env` file and fill in your values:
    ```
    ANTHROPIC_API_KEY=your_api_key_here
    OUTPUT_DIR=~/Documents/job_applications
    ```

4. **Add your input files**
    - Place your resume(s) in `inputs/resumes/` as `.docx` files
    - Paste the job description into `inputs/job_description.txt`
    - Optionally place your cover letter template at `inputs/cover_letter_template.docx`

---

## Usage

1. Copy and paste the job description into `inputs/job_description.txt`
2. Run the tool from your terminal:
    ```bash
    python main.py
    ```
3. Follow the prompts:
    - Review the tailored resume preview
    - Type `yes` to approve and continue, or `no` to provide feedback and regenerate
4. Once approved, all output files are saved to your `OUTPUT_DIR`
5. Repeat for each new job application

---

## Project Structure

```
job_assistant/
├── .env.example
├── .env                        
├── .gitignore
├── requirements.txt
├── README.md
├── main.py
├── agent.py                   
├── tools/
│   ├── file_tools.py
│   ├── analysis_tools.py
│   └── writing_tools.py
└── inputs/
    ├── job_description.txt
    ├── cover_letter_template.docx
    └── resumes/
        ├── Resume_1.docx
        ├── Resume_2.docx
        ├── Resume_3.docx
        └── Other resumes
```

---

## Output

All generated files are saved under your configures `OUTPUT_DIR`:

```
OUTPUT_DIR/
└── Company_Name/
    └── Job_Title/
        ├── resume.docx
        ├── cover_letter.docx
        ├── job_description.txt
        └── interview_prep.md
```

---

## Limitations
- **Resume formatting** - the tailored resume is exported as plain text inside a `.docx` file. You will need to apply your own formatting and layout before submitting.
- **Manual job description input** - the job description must be copy-pasted into `job_description.txt` manually. Support for direct job posting URLs is planned for a future version.