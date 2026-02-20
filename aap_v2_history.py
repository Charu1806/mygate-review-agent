
import streamlit as st
from review_agent_gemini_v2 import ask_question_with_evidence


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Review Intelligence Chat",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS (COLORS)
# -----------------------------
st.markdown("""
<style>

/* Headings Blue */
h1, h2, h3 {
    color: #1565C0;
}

/* Green Buttons */
.stButton > button {
    background-color: #2E7D32;
    color: black;
    border-radius: 8px;
    font-weight: 600;
}

/* Chat input styling */
[data-testid="stChatInput"] {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.title("🤖 Review Intelligence Chat")

# -----------------------------
# SESSION STATE (CHAT MEMORY)
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Hi! I can analyze review data for you.\n\nTry asking:\n- What are top complaints?\n- What do users love?\n- What should product fix first?"
        }
    ]

# -----------------------------
# CLEAR CHAT BUTTON
# -----------------------------
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# -----------------------------
# DISPLAY CHAT HISTORY
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# CHAT INPUT (BOTTOM)
# -----------------------------
prompt = st.chat_input("Ask about reviews...")

if prompt:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing reviews..."):
            result = ask_question_with_evidence(prompt)

            answer = result["answer"]
            reviews = result["reviews"]
            avg_rating = result["avg_rating"]
            keyword_counts = result["keyword_counts"]
            confidence = result["confidence"]
            topics = result["topics"]

            st.markdown(answer)

            st.divider()

            st.markdown("### 📊 Quick Signals")
            st.write(f"⭐ Avg Rating (evidence set): {avg_rating}")
            st.write(f"🧠 Confidence: {confidence}")

            st.write("🔑 Keyword Mentions:")
            st.json(keyword_counts)
            
            # ---------------- TOPICS ----------------
            if topics:
                st.divider()
                st.markdown("### 🧠 Top Themes Detected")

                for t in topics:
                    st.write(f"• {t}")		
            # ---------------- EVIDENCE ----------------
            

            st.divider()

            st.markdown("### 🔎 Top Evidence Reviews")

            for r in reviews[:5]:
                st.markdown(
                    f"⭐ {r.get('score','NA')} — {r.get('content','')[:200]}..."
                )
            


            # Save AI response
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

