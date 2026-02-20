import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from review_agent_gemini_v2 import ask_question_with_evidence

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Review Intelligence",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
st.sidebar.title("📊 Review Intelligence")

menu = st.sidebar.radio(
    "Navigation",
    ["💬 Ask Questions", "📈 Topic Trends Over Time"]
)

# ============================================================
# ===================== CHAT PAGE ============================
# ============================================================

if menu == "💬 Ask Questions":

    st.title("🤖 AI Review Intelligence")

    # Initialize chat memory
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hi 👋 Ask me anything about the reviews.\n\nExamples:\n- What should product fix first?\n- What are the biggest complaints?\n- What do users like most?"
            }
        ]

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # INPUT BOX (must be inside this block)
    prompt = st.chat_input("Ask about reviews...")

    if prompt:
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing reviews..."):
                result = ask_question_with_evidence(prompt)
                answer = result["answer"]
                st.markdown(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

elif menu == "📈 Topic Trends Over Time":

    st.title("📈 Topic Trends Over Time")

    try:
        df = pd.read_csv(
            "reviews_with_topics.csv",
            engine="python",
            on_bad_lines="skip"
        )

        df["at"] = df["at"].astype(str).str.replace("$", "", regex=False)
        df["at"] = pd.to_datetime(df["at"], errors="coerce")

        df = df.dropna(subset=["at"])
        df["month"] = df["at"].dt.to_period("M").astype(str)

        if "topic" not in df.columns:
            st.error("Topic column missing in CSV.")
        else:
            top_topics = df["topic"].value_counts().head(5).index
            df_filtered = df[df["topic"].isin(top_topics)]

            pivot = df_filtered.pivot_table(
                index="month",
                columns="topic",
                aggfunc="size",
                fill_value=0
            )

            if pivot.empty:
                st.warning("No trend data available.")
            else:
                st.line_chart(pivot)

    except Exception as e:
        st.error(f"Trend loading error: {e}")

