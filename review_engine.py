import pickle
import numpy as np
from google import genai

client = genai.Client(api_key="YOUR_API_KEY")

# ---------- Load embeddings once ----------
def load_store():
    with open("embeddings.pkl", "rb") as f:
        return pickle.load(f)

store = load_store()

# ---------- Cosine similarity ----------
def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot / (norm1 * norm2)

# ---------- Retrieve top reviews ----------
def get_top_reviews(question_embedding, top_k=5):
    scores = []

    for item in store:
        sim = cosine_similarity(question_embedding, item["embedding"])
        scores.append((sim, item))

    scores.sort(reverse=True, key=lambda x: x[0])
    return [x[1] for x in scores[:top_k]]

# ---------- Generate answer ----------
def generate_answer(question, reviews):
    review_text = "\n".join([r["content"] for r in reviews])

    prompt = f"""
    You are a senior product analyst.

    Question: {question}

    Reviews:
    {review_text}

    Provide prioritized, actionable insights.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

