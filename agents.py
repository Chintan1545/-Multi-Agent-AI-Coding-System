import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def problem_analyzer(prompt: str) -> str:
    """Analyze and structure the coding problem."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # supported Groq model
        messages=[
            {"role": "system",
             "content": "You are an expert AI coding assistant. Structure coding problems clearly with inputs, outputs, and constraints."},
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content

def code_generator(structured_problem: str) -> str:
    """Generate Python code with docstrings, type hints, and sample test cases."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system",
             "content": "You are an expert Python programmer. Generate optimized Python code with docstrings, type hints, sample test cases, and handle edge cases."},
            {"role": "user", "content": structured_problem}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content
