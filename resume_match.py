from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pdf_reader import extract_text_from_pdf

resume_text = extract_text_from_pdf("sample_resume.pdf")

job_description = """
Looking for a Java developer with knowledge of Spring Boot, SQL, Hibernate, REST APIs, and Git.
"""

vectorizer = TfidfVectorizer(stop_words="english")
vectors = vectorizer.fit_transform([resume_text, job_description])

similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
match_percentage = round(similarity * 100, 2)

print("Resume Match Percentage:", match_percentage)
