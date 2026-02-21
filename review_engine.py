import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
from dotenv import load_dotenv

# ---------------------------
# ENV + GEMINI SETUP
# ---------------------------

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------------------
# LOAD DATA + BUILD TF-IDF
# ---------------------------

CSV_FILE = "mygate_reviews_real.csv"

print("Loading review data...")
df = pd.read_csv(CSV_FILE)

df["content"] = df["content"].fillna("")

print("Building TF-IDF vectorizer...")
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

tfidf_matrix = vectorizer.fit_transform(df["content"])

print("TF-IDF ready.")

# ---------------------------
# CORE SEARCH FUNCTION
# ---------------------------

def get_top_reviews(question, top_k=8):
    """
    Returns top_k most similar reviews to question
    """

    question_vec = vectorizer.transform([question])
    similarities = cosine_similarity(question_vec, tfidf_matrix).flatten()

    top_indices = similarities.argsort()[-top_k:][::-1]

    top_reviews = df.iloc[top_indices].to_dict(orient="records")

    return top_reviews


# ---------------------------
# GEMINI ANALYST RESPONSE
# ---------------------------

def generate_answer(question, reviews):
    """
    Uses Gemini to generate executive-style insights
    """

    review_text = "\n\n".join(
        [f"Rating: {r.get('score')} | {r.get('content')}" for r in reviews]
    )

    prompt = f"""
You are a senior product analyst.

Based on the following user reviews, answer the question with:

1. Clear prioritized issues
2. Quantified signals where possible
3. What product team should fix first
4. Risk level (Low / Medium / High)

Question:
{question}

User Reviews:
{review_text}
"""

    response = model.generate_content(prompt)

    return response.text


# ---------------------------
# MAIN PUBLIC FUNCTION
# ---------------------------

def ask_question_with_evidence(question, top_k=8):

    top_reviews = get_top_reviews(question, top_k=top_k)

    answer = generate_answer(question, top_reviews)

    # quick signals
    ratings = [r.get("score", 0) for r in top_reviews if r.get("score")]

    avg_rating = round(np.mean(ratings), 2) if ratings else "NA"

    negative_ratio = (
        round(
            sum(1 for r in ratings if r <= 2) / len(ratings) * 100,
            2
        )
        if ratings else 0
    )

    return {
        "answer": answer,
        "evidence": top_reviews,
        "signals": {
            "avg_rating": avg_rating,
            "negative_percentage": negative_ratio,
            "review_count": len(top_reviews)
        }
    }
