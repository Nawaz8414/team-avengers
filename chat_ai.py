# chat_ai.py
import streamlit as st
from openai import OpenAI



client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://your-app-name.streamlit.app",
        "X-Title": "AI Jobseeker Platform"
    }
)

def generate_chat_response(user_message, resume_data, mode="jobseeker", chat_history=None):

    if chat_history is None:
        chat_history = []

    if mode == "jobseeker":
        system_prompt = """
You are an AI career coach.
Help jobseekers with resume improvements, career guidance,
interview preparation, and skill gap analysis.
Be conversational and detailed.
"""
    else:
        system_prompt = """
You are a professional recruiter.
Help HR teams evaluate candidates, shortlist resumes,
identify strengths & weaknesses, and suggest interview questions.
Be structured and professional.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"Resume Analysis:\n{resume_data}"}
    ]

    # ✅ FIX: map UI roles → API roles
    for role, content in chat_history:
        if role.lower() in ["you", "user"]:
            messages.append({"role": "user", "content": content})
        else:
            messages.append({"role": "assistant", "content": content})

    messages.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content