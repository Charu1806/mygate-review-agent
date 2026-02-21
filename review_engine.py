import pickle
import numpy as np
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def load_store():
    with open("embeddings.pkl", "rb") as f:
        return pickle.load(f)

store = load_store()

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def generate_answer(question, reviews):
    review_text = "\n".join([r["content"] for r in reviews])

    prompt = f"""
    You are a senior product analyst.
    Question: {question}
    Reviews:
    {review_text}
    Provide prioritized actionable insights.
    """

    response = model.generate_content(prompt)
    return response.text
