import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

function App() {
  const [resume, setResume] = useState(null);
  const [jd, setJd] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeResume = async () => {
    if (!resume || !jd.trim()) {
      alert("Please upload a resume and paste the job description.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_description", jd);

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      alert("Backend not running. Start FastAPI server first.");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <div className="hero">
        <h1>AI-Powered Resume Matcher</h1>
        <p>Upload your resume and compare it with a job description using AI/NLP-based scoring.</p>
      </div>

      <div className="card">
        <label>Upload Resume PDF</label>
        <input type="file" accept=".pdf" onChange={(e) => setResume(e.target.files[0])} />

        <label>Paste Job Description</label>
        <textarea
          rows="10"
          placeholder="Paste the job description here..."
          value={jd}
          onChange={(e) => setJd(e.target.value)}
        />

        <button onClick={analyzeResume} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>
      </div>

      {result && (
        <div className="result">
          <h2>Match Score: {result.final_score}%</h2>

          <div className="grid">
            <div className="box">
              <h3>Matching Skills</h3>
              <p>{result.matching_skills.length ? result.matching_skills.join(", ") : "No matching skills found"}</p>
            </div>

            <div className="box">
              <h3>Missing Skills</h3>
              <p>{result.missing_skills.length ? result.missing_skills.join(", ") : "No major missing skills found"}</p>
            </div>
          </div>

          <div className="box">
            <h3>AI Suggestions</h3>
            <ul>
              {result.feedback.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
