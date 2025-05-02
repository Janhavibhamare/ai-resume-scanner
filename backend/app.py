from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# Extract text from PDF
def extract_text_from_pdf(file_stream):
    text = ""
    with fitz.open(stream=file_stream.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# Extract Gmail ID
def extract_email(text):
    match = re.search(r'\b[A-Za-z0-9._%+-]+@gmail\.com\b', text)
    if match:
        return match.group(0)
    return "Unknown"

# Extract skills (basic keyword check)
def extract_skills(text):
    skills = ['python', 'java', 'javascript', 'html', 'css', 'react', 'angular', 'node', 'sql', 'docker']
    found_skills = [skill for skill in skills if skill in text.lower()]
    return found_skills

# Calculate cosine similarity score between job desc and resume
def calculate_match_score(resume_text, job_description):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_description])
    cosine_sim = cosine_similarity(vectors[0:1], vectors[1:2])
    return cosine_sim[0][0] * 100  # Score between 0 and 100

# Resume scan API
@app.route("/scan", methods=["POST"])
def scan_resume():
    resume_file = request.files.get("resume")
    job_description = request.form.get("job_description")

    if not resume_file:
        return jsonify({"error": "No resume uploaded"}), 400

    resume_text = extract_text_from_pdf(resume_file)
    name_or_email = extract_email(resume_text)
    skills = extract_skills(resume_text)

    match_score = 0
    if job_description:
        match_score = calculate_match_score(resume_text, job_description)

    # If score is 0, show "Skills not found"
    if round(match_score, 2) == 0:
        skills = ["Skills not found"]

    result = {
        "name": name_or_email,
        "skills_found": skills,
        "match_score": round(match_score, 2)
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
