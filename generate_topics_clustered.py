import pandas as pd
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
from review_agent_gemini_v2 import generate_topic_label_with_llm

# ==============================
# CONFIG
# ==============================

INPUT_FILE = "mygate_reviews_real.csv"
OUTPUT_FILE = "reviews_with_topics.csv"

NEG_CLUSTERS = 12
POS_CLUSTERS = 8

# ==============================
# LOAD DATA
# ==============================

print("Loading reviews...")

df = pd.read_csv(
    INPUT_FILE,
    engine="python",
    on_bad_lines="skip"
)

df["content"] = df["content"].astype(str)

# Remove empty reviews
df = df[df["content"].str.strip() != ""]

# ==============================
# SPLIT BY SENTIMENT (RATING)
# ==============================

df_neg = df[df["score"] <= 3].copy()
df_pos = df[df["score"] >= 4].copy()

print(f"Negative reviews: {len(df_neg)}")
print(f"Positive reviews: {len(df_pos)}")

# ==============================
# GENERATE LOCAL EMBEDDINGS
# ==============================

print("Generating embeddings...")

model = SentenceTransformer("all-MiniLM-L6-v2")

neg_embeddings = model.encode(
    df_neg["content"].tolist(),
    show_progress_bar=True
)

pos_embeddings = model.encode(
    df_pos["content"].tolist(),
    show_progress_bar=True
)

# ==============================
# CLUSTER NEGATIVE REVIEWS
# ==============================

print(f"Clustering {NEG_CLUSTERS} negative clusters...")

kmeans_neg = KMeans(
    n_clusters=NEG_CLUSTERS,
    random_state=42,
    n_init=10
)

df_neg["cluster"] = kmeans_neg.fit_predict(neg_embeddings)

# ==============================
# CLUSTER POSITIVE REVIEWS
# ==============================

print(f"Clustering {POS_CLUSTERS} positive clusters...")

kmeans_pos = KMeans(
    n_clusters=POS_CLUSTERS,
    random_state=42,
    n_init=10
)

df_pos["cluster"] = kmeans_pos.fit_predict(pos_embeddings)

# Offset positive cluster IDs
df_pos["cluster"] = df_pos["cluster"] + NEG_CLUSTERS

# Merge back
df_all = pd.concat([df_neg, df_pos])

# ==============================
# LABEL CLUSTERS WITH GEMINI
# ==============================

cluster_topic_map = {}

total_clusters = NEG_CLUSTERS + POS_CLUSTERS

print("Labeling clusters using Gemini...")

for cluster_id in range(total_clusters):

    cluster_reviews = df_all[df_all["cluster"] == cluster_id]["content"].tolist()

    sample_reviews = cluster_reviews[:10]

    topic_label = generate_topic_label_with_llm(sample_reviews)

    cluster_topic_map[cluster_id] = topic_label

    print(f"Cluster {cluster_id} → {topic_label}")

# ==============================
# ASSIGN TOPICS
# ==============================

df_all["topic"] = df_all["cluster"].map(cluster_topic_map)

# ==============================
# SAVE FILE (SAFE CSV FORMAT)
# ==============================

df_all.to_csv(
    OUTPUT_FILE,
    index=False,
    quoting=1
)

print(f"\nDone. {OUTPUT_FILE} created successfully.")

