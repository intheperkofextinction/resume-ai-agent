import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# ── Load API key from .env ────────────────────────────────
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ── Read your master resume JSON ──────────────────────────
def load_resume():
    with open("master_resume.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ── Get job description from terminal ────────────────────
def get_jd():
    print("\nPaste the job description.")
    print("When finished type END on a new line and press Enter:\n")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)

# ── Build resume prompt ───────────────────────────────────
def resume_prompt(resume, jd, company, role):
    return f"""You are an expert resume writer specializing in financial analytics and data roles.

Using ONLY the information in the master resume JSON below,
generate a tailored, professional resume for the job description provided.

MASTER RESUME:
{json.dumps(resume, indent=2)}

JOB DESCRIPTION:
{jd}

COMPANY: {company or 'Not specified'}
ROLE: {role or 'Not specified'}

INSTRUCTIONS:
- Select the 5-6 most relevant projects that match this JD
- Write a tailored summary specific to this role and company
- Reorder and emphasize skills the JD prioritizes
- Highlight domain knowledge most relevant to this role
- Mention the published book and AI agent — this are strong differentiator
- Only use facts from the master resume — never invent anything
- The summary must NOT mention the company name or say "excited to apply" — write it as a timeless professional statement
- Use the actual bullet points from the master resume for each project — do not summarize them
- In domain knowledge only list things the candidate has actual project evidence for
- In education list self-directed study BEFORE the engineering degree
- Every project must include at least one specific metric or number
- For each project selected, follow any resume_instructions field if present
- Format cleanly with these sections in order:
  SUMMARY | DOMAIN KNOWLEDGE | SKILLS | PUBLICATION  | PROJECTS | EXPERIENCE | EDUCATION

Generate the complete tailored resume now:"""

# ── Build cover letter prompt ─────────────────────────────
def cover_prompt(resume, jd, company, role):
    return f"""You are an expert cover letter writer for financial analytics and data roles.

Using ONLY the information in the master resume JSON below,
write a compelling, human cover letter.

MASTER RESUME:
{json.dumps(resume, indent=2)}

JOB DESCRIPTION:
{jd}

COMPANY: {company or 'this company'}
ROLE: {role or 'this position'}

INSTRUCTIONS:
- Open with a strong compelling hook — never start with 'I am writing to apply'
- Paragraph 1: Hook + who you are + your strongest differentiator
- Paragraph 2: 2-3 specific projects from the resume most relevant to this JD
- Paragraph 3: Mention the published book + the self-taught journey as a strength + created an AI agent
- Paragraph 4: Why this company specifically + clear call to action
- Tone: professional but human — confident without being arrogant
- Length: 4 paragraphs only
- Never invent any fact not in the master resume
- Never use the word "excited" more than once in the entire letter
- Include at least one specific number from the projects (₹11.2B, 759K loans, etc.)
- Paragraph 4 must reference something specific from the JD itself — a responsibility, a team structure, or a stated goal — not generic praise about the company
- Close with something like: "I'd welcome a conversation about how my work translates directly to NovaPay's credit underwriting challenges."
- Closing must be confident and direct — not "please feel free to contact me"
- CRITICAL: Never claim experience with skills not evidenced in the master resume projects
- Do not mention cohort analysis, vintage analysis, IFRS 9, or logistic regression ML unless they appear in the project bullets

Generate the complete cover letter now:"""

# ── Build JD analysis prompt ──────────────────────────────
def analyze_prompt(resume, jd):
    return f"""Analyze this job description against the candidate's master resume.

MASTER RESUME:
{json.dumps(resume, indent=2)}

JOB DESCRIPTION:
{jd}

Provide:
1. TOP MATCHING STRENGTHS — where this candidate fits strongly
2. KEY JD KEYWORDS — most important terms to emphasize
3. HONEST GAPS — what's missing or weak vs the JD
4. BEST PROJECTS TO HIGHLIGHT — which 3 projects and why
5. LIKELY INTERVIEW QUESTIONS — 5 questions with brief answer angles

Be specific and honest:"""

# ── Call Gemini API ───────────────────────────────────────
def call_gemini(prompt):
    print("\nGenerating...")
    time.sleep(3)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )
    return response.choices[0].message.content

# ── Save output to file ───────────────────────────────────
def save(content, filename):
    Path("outputs").mkdir(exist_ok=True)
    path = f"outputs/{filename}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved → {path}")
    return content

# ── Main program ──────────────────────────────────────────
def main():
    print("=" * 45)
    print("   AMAL'S RESUME AI AGENT — powered by Gemini")
    print("=" * 45)

    # Load resume
    resume = load_resume()
    print(f"\nResume loaded — {len(resume['projects'])} projects ready")

    # Get job details
    company = input("\nCompany name  (Enter to skip): ").strip()
    role    = input("Role title    (Enter to skip): ").strip()

    # Get JD
    jd = get_jd()
    if not jd.strip():
        print("No JD entered. Exiting.")
        return

    # Menu
    print("\nWhat do you want to generate?")
    print("1 — Tailored resume only")
    print("2 — Cover letter only")
    print("3 — Both resume and cover letter")
    print("4 — Full JD analysis + both")
    choice = input("\nEnter 1, 2, 3 or 4: ").strip()

    # Clean filename base
    base = f"{company or 'company'}_{role or 'role'}".replace(" ", "_").lower()

    # Generate based on choice
    if choice == "4":
        print("\nAnalyzing JD...")
        analysis = call_gemini(analyze_prompt(resume, jd))
        save(analysis, f"analysis_{base}.txt")
        print("\n── JD Analysis ──")
        print(analysis[:600] + "\n...")

    if choice in ["1", "3", "4"]:
        resume_out = call_gemini(resume_prompt(resume, jd, company, role))
        save(resume_out, f"resume_{base}.txt")
        print("\n── Resume Preview ──")
        print(resume_out[:500] + "\n...")

    if choice in ["2", "3", "4"]:
        cover_out = call_gemini(cover_prompt(resume, jd, company, role))
        save(cover_out, f"cover_{base}.txt")
        print("\n── Cover Letter Preview ──")
        print(cover_out[:500] + "\n...")

    print("\n✓ Done. Check your outputs/ folder.")
    print(f"  Files saved with prefix: {base}")

# ── Entry point ───────────────────────────────────────────
if __name__ == "__main__":
    main()