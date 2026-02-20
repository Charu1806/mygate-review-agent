from fastapi import FastAPI
from pydantic import BaseModel
from review_agent_gemini_v2 import ask_question_with_evidence

app = FastAPI()

# Request schema
class QuestionRequest(BaseModel):
    question: str

# Health check route
@app.get("/")
def root():
    return {"status": "AI Review API running"}

# Main AI route
@app.post("/ask")
def ask_question(data: QuestionRequest):

    result = ask_question_with_evidence(data.question)

    return {
        "answer": result["answer"],
        "avg_rating": result["avg_rating"],
        "confidence": result["confidence"],
        "topics": result["topics"],
        "keyword_counts": result["keyword_counts"],
        "top_reviews": [
            {
                "score": r.get("score"),
                "content": r.get("content")
            }
            for r in result["reviews"][:5]
        ]
    }

