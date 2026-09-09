import re
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="GitHub Gone Wrong - Gemini Assistant", page_icon="🤖")
st.title("GitHub Gone Wrong: Gemini AI Mentor")
st.write("Ask conceptual questions about errors, debugging strategies, or Git workflows!")

@st.cache_resource
def get_gemini_client():
    return genai.Client()

client = get_gemini_client()

SYSTEM_INSTRUCTION = """
You are an expert technical mentor for the "GitHub Gone Wrong" debugging event. 
Your goal is to help participants understand errors and concepts conceptually.
CRITICAL RULES:
1. NEVER write code snippets, patches, function fixes, or git diff solutions.
2. NEVER give direct code solutions to repository issues.
3. Guide users using high-level concepts, architectural explanations, or leading questions.
"""

def contains_forbidden_code(text: str) -> bool:
    """Output Guardrail: Intercepts code blocks or git diff patches."""
    if "```" in text:
        return True
    if re.search(r"^\+[ \t].+$", text, re.MULTILINE) and re.search(r"^-[ \t].+$", text, re.MULTILINE):
        return True
    return False

# Initialize chat session safely with gemini-3.6-flash (omitting unsupported params like temperature)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model="gemini-3.6-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION
        )
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Chat Input
if user_prompt := st.chat_input("Ask a question about your repository issue..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking conceptually..."):
            try:
                response = st.session_state.chat_session.send_message(user_prompt)
                answer = response.text
                
                if contains_forbidden_code(answer):
                    answer = "🛡️ **Guardrail Triggered:** I can explain how this component works, how Git handles this scenario, or help you trace the error logic, but I cannot write the code fix for you. What does your current error stack trace look like?"
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                if "client has been closed" in str(e) or "closed" in str(e) or "404" in str(e):
                    st.session_state.chat_session = client.chats.create(
                        model="gemini-3.6-flash",
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION
                        )
                    )
                    response = st.session_state.chat_session.send_message(user_prompt)
                    answer = response.text
                    if contains_forbidden_code(answer):
                        answer = "🛡️ **Guardrail Triggered:** I can explain how this component works, how Git handles this scenario, or help you trace the error logic, but I cannot write the code fix for you. What does your current error stack trace look like?"
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Error communicating with Gemini API: {e}")
                    