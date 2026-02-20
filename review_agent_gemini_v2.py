import os
import pandas as pd
import numpy as np
import time
import pickle
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from google import genai

from collections import Counter

from sklearn.cluster import KMeans
import re

# ----------------------------
# CONFIG
# ----------------------------
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={'api_version': 'v1beta'}
)

EMBED_MODEL = "gemini-embedding-001"
QA_MODEL = "gemini-2.5-flash"

DATA_FILE = "mygate_reviews_real.csv"
EMBEDDING_FILE = "review_embeddings.pkl"
local_embed_model = SentenceTransformer("all-MiniLM-L6-v2")


# ----------------------------
# LOAD REVIEWS
# ----------------------------
def load_reviews(csv_path):
    df = pd.read_csv(csv_path)

    df = df.dropna(subset=["content"])
    df["content"] = df["content"].astype(str)

    if "at" in df.columns:
        df["at"] = pd.to_datetime(df["at"], errors="coerce")

    return df


# ----------------------------
# EMBEDDING
# ----------------------------
def get_embedding(text):

    text = str(text)[:2000]

    embedding = local_embed_model.encode(text)

    return embedding


# ----------------------------
# BUILD EMBEDDINGS
# ----------------------------

#CHECKPOINT_FILE = "embedding_checkpoint.pkl"

#def build_embeddings(df):

    # Load checkpoint if exists
 #   if os.path.exists(CHECKPOINT_FILE):
  #      print("Loading checkpoint...")
   #     with open(CHECKPOINT_FILE, "rb") as f:
    #        data = pickle.load(f)
     #       embeddings = data["embeddings"]
      #      start_index = data["index"]
   # else:
    #    embeddings = []
     #   start_index = 0

    #print(f"Starting from index: {start_index}")
#
 #   for i in range(start_index, len(df)):
#
 #       text = df.iloc[i]["content"]
#
 #       try:
  #          emb = get_embedding(text)
   #         embeddings.append(emb)
#
 #       except Exception as e:
  #          print("Quota hit. Saving checkpoint...")
   #         with open(CHECKPOINT_FILE, "wb") as f:
    #            pickle.dump({
     #               "embeddings": embeddings,
      #              "index": i
       #         }, f)
        #    raise e
#
 #       # Save checkpoint every 20 reviews
  #      if i % 20 == 0:
   #         print(f"Processed {i}")
    #        with open(CHECKPOINT_FILE, "wb") as f:
     #           pickle.dump({
      #              "embeddings": embeddings,
       #             "index": i
        #        }, f)
#

    # Final save
 #   embeddings = np.array(embeddings)

  #  with open(EMBEDDING_FILE, "wb") as f:
   #     pickle.dump({
    #        "embeddings": embeddings,
     #       "reviews": df.to_dict("records")
      #  }, f)

    #print("✅ FINAL embeddings saved!")

    # Remove checkpoint after success
    #if os.path.exists(CHECKPOINT_FILE):
     #   os.remove(CHECKPOINT_FILE)

# ----------------------------
# LOAD EMBEDDINGS
# ----------------------------
#def load_embeddings():
 #   with open(EMBEDDING_FILE, "rb") as f:
  #      return pickle.load(f)


#import pandas as pd
#import pickle
#from sentence_transformers import SentenceTransformer

#EMBEDDING_FILE = "review_embeddings.pkl"
#DATA_FILE = "mygate_reviews_real.csv"


# ----------------------------
# BUILD EMBEDDINGS
# ----------------------------


def build_embeddings():

    print("Building metadata-aware embedding store...")

    df = pd.read_csv(DATA_FILE)
    df["content"] = df["content"].astype(str)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(
        df["content"].tolist(),
        show_progress_bar=True
    )

    store = []

    for i, row in df.iterrows():

        store.append({
            "embedding": embeddings[i],
            "content": row["content"],
            "score": row.get("score"),
            "date": row.get("at"),
            "appVersion": row.get("appVersion"),
            "reviewId": row.get("reviewId")
        })

    with open(EMBEDDING_FILE, "wb") as f:
        pickle.dump(store, f)

    print("Embedding store saved.")


def load_embeddings():

    try:
        with open(EMBEDDING_FILE, "rb") as f:
            return pickle.load(f)
    except:
        build_embeddings()
        return load_embeddings()




# ----------------------------
# RETRIEVAL
# ----------------------------
#def get_top_reviews(question, store, top_k=10):
#
 #   q_emb = get_embedding(question)
#
 #   sims = cosine_similarity(
  #      [q_emb],
   #     store["embeddings"]
    #)[0]
#
 #   top_idx = np.argsort(sims)[-top_k:][::-1]
#
 #   return [store["reviews"][i] for i in top_idx]


#import numpy as np
#from sklearn.metrics.pairwise import cosine_similarity
#from sentence_transformers import SentenceTransformer

def get_top_reviews(question, store, top_k=8):

    model = SentenceTransformer("all-MiniLM-L6-v2")

    query_embedding = model.encode([question])[0]

    similarities = []

    for item in store:
        sim = cosine_similarity(
            [query_embedding],
            [item["embedding"]]
        )[0][0]

        similarities.append(sim)

    top_indices = np.argsort(similarities)[-top_k:][::-1]

    return [store[i] for i in top_indices]




# ----------------------------
# QA GENERATION
# ----------------------------
#def generate_answer(question, top_reviews):
#
 #   context = "\n\n".join([
  #      f"- {r.get('content','')} "
   #     f"(Rating: {r.get('score','NA')}, "
    #    f"Date: {r.get('at','NA')}, "
     #   f"Version: {r.get('appVersion','NA')})"
      #  for r in top_reviews
   # ])
#
 #   prompt = f"""
#You are a product insights analyst analyzing MyGate app user reviews.

#Use ONLY the reviews below to answer.

#If not enough evidence, say so.

#REVIEWS:
#{context}
#
#QUESTION:
#{question}
#
#Give concise PM-style insight.
#"""
#
 #   response = client.models.generate_content(
  #      model=QA_MODEL,
   #     contents=prompt
   # )

    #return response.text


def generate_answer(question, top_reviews):

    if not top_reviews:
        return "No relevant reviews found."

    formatted_reviews = ""

    for r in top_reviews:
        formatted_reviews += f"""
Rating: {r.get("score")}
Review: {r.get("content")}
---
"""

    prompt = f"""
You are a senior product manager analyzing customer reviews.

Question:
{question}

Relevant Reviews:
{formatted_reviews}

Instructions:
- Be decisive.
- Do NOT summarize vaguely.
- Identify the most critical issue if prioritization is required.
- Use rating distribution as signal of severity.
- Focus on business impact.

Structure your response EXACTLY as:

1. Core Finding
(1-2 clear sentences)

2. Evidence Patterns
(2-3 specific recurring issues)

3. Impact
(Why this matters for product/business)

4. Recommendation
(What should be done first)

Avoid generic phrases like "users report some issues".
Be specific and analytical.
"""

    response = client.models.generate_content(
        model=QA_MODEL,
        contents=prompt
    )

    return response.text.strip()

#_____________________________
#generate_topic_label_with_llm
#_____________________________

def generate_topic_label_with_llm(cluster_texts):

    try:
        sample_text = "\n".join(cluster_texts[:5])

        prompt = f"""
You are analyzing app reviews.

Below are multiple reviews that talk about a similar issue or theme.

Reviews:
{sample_text}

Task:
Summarize the COMMON THEME in 3-6 words max.

Rules:
- Focus on product feature or problem
- Avoid generic words like "good", "nice", "useful"
- Be specific (example: Gate Access Delay, Delivery OTP Failure, App Performance Slow)

Return ONLY the theme phrase.
"""

        response = client.models.generate_content(
            model=QA_MODEL,
            contents=prompt
        )

        return response.text.strip()

    except Exception:
        return "General User Feedback"

#_____________________________
#Add Topic Extraction Function
#_____________________________

def extract_topics_from_reviews(top_reviews, n_topics=3):

    if len(top_reviews) < n_topics:
        n_topics = max(1, len(top_reviews))

    texts = [r.get("content", "") for r in top_reviews]

    embeddings = local_embed_model.encode(texts)

    # Cluster reviews
    kmeans = KMeans(n_clusters=n_topics, random_state=42, n_init=10)
    labels = kmeans.fit_predict(embeddings)

    # Simple keyword extraction per cluster
    topics = []

    for cluster_id in range(n_topics):

        cluster_texts = [
            texts[i]
            for i in range(len(texts))
            if labels[i] == cluster_id
        ]

        combined = " ".join(cluster_texts).lower()

        words = re.findall(r'\b[a-z]{4,}\b', combined)

        stopwords = {
            "that","this","with","from","have","they","there",
            "their","about","after","before","when","where",
            "which","while","would","should","could"
        }

        words = [w for w in words if w not in stopwords]

        counts = Counter(words)

        top_words = [w for w,_ in counts.most_common(3)]

        topic_label = " ".join(top_words)
        
        topic_label = generate_topic_label_with_llm(cluster_texts)        

        topics.append(topic_label)

    return topics

#_____________________________
#ASK QUESTION WITH EVIDENCE
#_____________________________


def ask_question_with_evidence(question, top_k=8):

    store = load_embeddings()
    if "fix" in question.lower() or "issue" in question.lower():
        candidate_reviews = [r for r in store if r["score"] <= 3]
    else:
        candidate_reviews = store

    top_reviews = get_top_reviews(question, candidate_reviews, top_k)


    #top_reviews = get_top_reviews(question, store, top_k=top_k)

    answer = generate_answer(question, top_reviews)

    # -------------------
    # SIGNALS
    # -------------------

    ratings = [
        r.get("score", 0)
        for r in top_reviews
        if r.get("score") is not None
    ]

    avg_rating = round(np.mean(ratings), 2) if ratings else "NA"

    # keyword signal
    text_blob = " ".join([r.get("content", "") for r in top_reviews]).lower()

    keywords = ["gate", "otp", "delivery", "visitor", "app", "slow", "crash"]

    keyword_counts = {
        k: text_blob.count(k)
        for k in keywords
    }

    # confidence heuristic
    if len(top_reviews) >= 6:
        confidence = "High"
    elif len(top_reviews) >= 3:
        confidence = "Medium"
    else:
        confidence = "Low"

    # -------------------------
    # TOPIC DETECTION
    # -------------------------
    try:
        topics = extract_topics_from_reviews(
            top_reviews,
            n_topics=3
        )
    except Exception:
        topics = []

    return {
        "answer": answer,
        "reviews": top_reviews,
        "avg_rating": avg_rating,
        "keyword_counts": keyword_counts,
        "confidence": confidence,
        "topics": topics
    }


# ----------------------------
# MAIN QA FUNCTION
# ----------------------------
def ask_question(question):

    store = load_embeddings()

    top_reviews = get_top_reviews(question, store)

    answer = generate_answer(question, top_reviews)

    return answer


# ----------------------------
# RUNNER
# ----------------------------
if __name__ == "__main__":

    CSV_PATH = "mygate_reviews_real.csv"

    if not os.path.exists(EMBEDDING_FILE):
        print("Building embeddings first time...")
        df = load_reviews(CSV_PATH)
        build_embeddings()

    print("\n✅ Review AI Agent Ready\n")

    while True:
        q = input("Ask question (or exit): ")

        if q.lower() == "exit":
            break

        ans = ask_question(q)
        print("\n📊 Answer:\n", ans)

