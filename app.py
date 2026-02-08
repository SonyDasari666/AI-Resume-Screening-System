from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import os

app = Flask(__name__)

# ---------------- SKILLS LIST ----------------
SKILLS = [
    "java", "python", "sql", "mysql", "spring", "spring boot",
    "hibernate", "html", "css", "javascript", "react",
    "flask", "machine learning", "data structures",
    "git", "rest api", "docker", "kubernetes"
]

# ---------------- PDF TEXT EXTRACTION ----------------
def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# ---------------- SKILL EXTRACTION ----------------
def extract_skills(text):
    text = text.lower()
    found_skills = set()

    for skill in SKILLS:
        if skill in text:
            found_skills.add(skill)

    return list(found_skills)


# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/match", methods=["POST"])
def match_resume():
    resume = request.files["resume"]
    job_description = request.form["job_description"]

    resume_text = extract_text_from_pdf(resume)

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_description])

    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    match_percentage = round(similarity * 100, 2)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    if len(jd_skills) > 0:
        missing_skills = list(set(jd_skills) - set(resume_skills))
    else:
        missing_skills = []


    # DEBUG OUTPUT (shows in terminal)
    print("Resume Skills:", resume_skills)
    print("JD Skills:", jd_skills)
    print("Missing Skills:", missing_skills)

    return render_template(
        "index.html",
        match_percentage=match_percentage,
        missing_skills=missing_skills
    )

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=True)
