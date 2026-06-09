# AI-Powered Resume Screening & Job Matching Assistant

An AI-powered web application that compares a candidate resume with a job description, extracts key skills, calculates a job-fit score, and generates personalized improvement suggestions.

## Features
- Resume PDF upload
- Job description input
- Resume text extraction
- Skill extraction
- Keyword gap analysis
- Match score calculation
- AI-generated resume improvement suggestions
- React dashboard with FastAPI backend

## Tech Stack
Frontend: React, Vite, JavaScript, CSS  
Backend: Python, FastAPI  
AI/LLM: Gemini API / OpenAI API-ready prompt structure  
NLP: TF-IDF similarity, keyword matching  
PDF Parsing: PyMuPDF  

## Project Flow
1. User uploads resume PDF.
2. User pastes job description.
3. Backend extracts resume text.
4. System identifies matching and missing skills.
5. Similarity score is calculated.
6. LLM generates resume improvement suggestions.
7. Results are shown on dashboard.

## Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Create a `.env` file:
```env
GEMINI_API_KEY=your_api_key_here
```

The project works even without an API key using rule-based suggestions.

## Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Resume Points
- Built an AI-powered resume screening and job matching assistant that compares resumes with job descriptions using NLP and LLM-based recommendations.
- Implemented resume PDF parsing, skill extraction, keyword gap analysis, and job-fit scoring using FastAPI and Python.
- Developed a React dashboard for resume upload, JD comparison, match score visualization, and AI-generated feedback.
- Integrated Gemini API-ready prompt flow to generate personalized resume improvement suggestions.

## Future Enhancements
- Add authentication
- Store previous resume scans
- Add recruiter dashboard
- Use vector database like ChromaDB
- Deploy backend on Render and frontend on Vercel
