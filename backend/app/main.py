from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import fitz
import re
import os
import requests
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

app = FastAPI(title="AI Resume Matcher API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SKILLS = [
    "python", "java", "javascript", "typescript", "react", "node.js", "node",
    "express", "sql", "mysql", "postgresql", "mongodb", "aws", "docker",
    "fastapi", "flask", "rest api", "api", "machine learning", "deep learning",
    "nlp", "git", "github", "html", "css", "tailwind", "pandas", "numpy",
    "scikit-learn", "data structures", "algorithms",

    "software development", "software engineering", "coding", "debugging",
    "testing", "test cases", "automation", "quality assurance", "sdlc",
    "requirements analysis", "system design", "root cause analysis",
    "documentation", "client requirements", "application development",
    "maintenance", "performance improvement", "problem solving",
    "team collaboration", "status reporting", "customer communication"
]

def extract_pdf_text(file_bytes: bytes) -> str:
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text

def extract_skills(text: str):
    text = clean_text(text)
    found = []
    for skill in SKILLS:
        if skill in text:
            found.append(skill)
    return sorted(set(found))

def calculate_similarity(resume_text: str, jd_text: str) -> int:
    if not resume_text.strip() or not jd_text.strip():
        return 0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1
    )
    vectors = vectorizer.fit_transform([resume_text.lower(), jd_text.lower()])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    return round(score * 100)

def generate_rule_based_feedback(missing_skills, score):
    suggestions = []
    if score < 40:
        suggestions.append("Your resume needs stronger alignment with the job description. Add relevant project and skill keywords from the JD.")
    elif score < 70:
        suggestions.append("Your resume has partial alignment. Improve bullet points by adding measurable impact and role-specific keywords.")
    else:
        suggestions.append("Your resume is well aligned. Improve it further by adding metrics, deployment links, and stronger action verbs.")

    if missing_skills:
        suggestions.append("Consider adding or learning these missing skills if relevant: " + ", ".join(missing_skills[:8]) + ".")
    suggestions.append("Add project outcomes such as performance improvement, accuracy, API response time, or number of users/features.")
    suggestions.append("Use keywords from the job description naturally in your skills and project sections.")
    return suggestions

def generate_llm_feedback(resume_text: str, jd_text: str, missing_skills):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    prompt = f"""
You are an expert technical recruiter. Analyze the resume against the job description.
Give 5 short, practical suggestions to improve the resume.

Missing skills: {missing_skills}

Resume:
{resume_text[:3500]}

Job Description:
{jd_text[:2500]}
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, json=payload, timeout=20)
        data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return [line.strip("-• ").strip() for line in text.split("\n") if line.strip()][:6]
    except Exception:
        return None

@app.get("/")
def home():
    return {"message": "AI Resume Matcher API is running"}

@app.post("/analyze")
async def analyze_resume(resume: UploadFile = File(...), job_description: str = Form(...)):
    file_bytes = await resume.read()
    resume_text = extract_pdf_text(file_bytes)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    matching_skills = sorted(set(resume_skills).intersection(set(jd_skills)))
    missing_skills = sorted(set(jd_skills).difference(set(resume_skills)))

    similarity_score = calculate_similarity(resume_text, job_description)

    skill_score = 0
    if jd_skills:
        skill_score = round((len(matching_skills) / len(jd_skills)) * 100)

    final_score = round((similarity_score * 0.25) + (skill_score * 0.75))

    llm_feedback = generate_llm_feedback(resume_text, job_description, missing_skills)
    feedback = llm_feedback if llm_feedback else generate_rule_based_feedback(missing_skills, final_score)

    return {
        "final_score": final_score,
        "similarity_score": similarity_score,
        "skill_score": skill_score,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "feedback": feedback
    }
