import streamlit as st
import re
from agents import problem_analyzer, code_generator
from sandbox import run_code_safely

# 🔹 Extract Python code from markdown
def extract_code(text: str):
    pattern = r"```python(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


# Streamlit UI

st.set_page_config(page_title="Multi-Agent Coding", layout="centered")
st.title("🤖 Multi-Agent AI Coding System ")

user_input = st.text_area(
    "Enter your coding problem:",
    height=150,
    placeholder="Example: Write a function to check if a number is a palindrome."
)

if st.button("Generate & Execute"):

    if not user_input.strip():
        st.warning("Please enter a coding problem.")
    else:
        # 1️⃣ Problem Analyzer
        with st.spinner("Analyzing problem..."):
            structured_problem = problem_analyzer(user_input)
            st.subheader("📝 Structured Problem")
            st.write(structured_problem)

        # 2️⃣ Code Generator
        with st.spinner("Generating Python solution..."):
            code_response = code_generator(structured_problem)
            st.subheader("💻 Generated Solution")
            st.markdown(code_response)

        # 3️⃣ Extract & Execute Code
        code = extract_code(code_response)
        if code:
            st.subheader("▶ Extracted Python Code")
            st.code(code, language="python")

            with st.spinner("Executing code..."):
                result = run_code_safely(code)
            st.subheader("🚀 Execution Result")
            st.text(result)
        else:
            st.info("No Python code block found.")
