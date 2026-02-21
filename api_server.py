from fastapi import FastAPI
from review_engine import generate_answer
import pandas as pd
from pydantic import BaseModel



app = FastAPI()

@app.get("/")
def health():
    return {"status": "running"}

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QuestionRequest):
    result = generate_answer(request.question)
    return result

@app.get("/daily-summary")
def daily_summary():
    df = pd.read_csv("mygate_reviews_real.csv")

    df["date"] = pd.to_datetime(df["at"], errors="coerce").dt.date
    latest_date = df["date"].max()

    latest_df = df[df["date"] == latest_date]

    avg_rating = round(latest_df["score"].mean(), 2)
    total_reviews = len(latest_df)
    negative_pct = round((latest_df["score"] <= 2).mean() * 100, 2)

    return {
        "date": str(latest_date),
        "avg_rating": avg_rating,
        "total_reviews": total_reviews,
        "negative_percentage": negative_pct
    }

@app.get("/trend")
def topic_trend():
    df = pd.read_csv("reviews_with_topics.csv")

    df["date"] = pd.to_datetime(df["at"]).dt.date

    trend = (
        df.groupby(["date", "topic"])
        .size()
        .reset_index(name="count")
    )

    return trend.to_dict(orient="records")

