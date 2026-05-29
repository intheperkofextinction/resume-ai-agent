# Resume AI Agent



An AI-powered job application agent that generates tailored resumes 

and cover letters by matching a master resume against any job description.



## What It Does



- Reads a structured master resume from a JSON file

- Takes any job description as input

- Generates a tailored resume highlighting the most relevant projects

- Generates a personalized cover letter

- Performs full JD analysis with gap identification and interview prep

- Saves all outputs as text files locally



## How It Works



1. Master resume stored as structured JSON with projects, skills, 

&#x20;  domain knowledge, and keywords

2. Job description pasted directly into terminal

3. LLM (Llama 3.3 70B via Groq API) reads both and generates 

&#x20;  tailored content using prompt engineering

4. Outputs saved to local outputs/ folder



## Tech Stack



- Python

- Groq API (Llama 3.3 70B)

- python-dotenv

- JSON



## Setup



1. Clone the repo

2. Install dependencies:

&#x20;  pip install groq python-dotenv

3. Create a .env file:

&#x20;  GROQ\_API\_KEY=your-key-here

4. Add your master\_resume.json

5. Run:

&#x20;  python resume\_agent.py



## Project Structure



resume\_agent/

&#x20;   resume\_agent.py       — main agent

&#x20;   master\_resume.json    — your resume data (not included)

&#x20;   .env                  — API key (not included)

&#x20;   outputs/              — generated files appear here



## Why I Built This



Applying to jobs as a self-taught analyst means every application 

needs to tell a specific story. I built this to reduce application 

prep time from 45 minutes to under 10 minutes while improving 

relevance and quality.

