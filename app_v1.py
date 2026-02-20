import streamlit as st
from review_agent_gemini_v2 import ask_question

st.set_page_config(page_title="Review AI", page_icon="🤖")

st.title("🤖 Review Intelligence AI")
st.write("Ask questions about MyGate reviews")

question = st.text_input("Ask a question about reviews")

if st.button("Ask"):

    if question.strip() == "":
        st.warning("Please enter a question")
    else:
        with st.spinner("Analyzing reviews..."):
            answer = ask_question(question)

        st.subheader("Answer")
        st.write(answer)

