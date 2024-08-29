import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")

# Streamlit UI setup
st.set_page_config(page_title="Stress Management Q&A Assistant")

# Custom CSS with animations and layout
st.markdown(
    """
    <style>
    .chat-container {
        width: 400px;
        padding: 20px;
        background-color: #f1f1f1;
        border-radius: 10px;
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
        position: fixed;
        top: 20px;
        right: 20px;
        max-height: 80vh;
        overflow-y: auto;
    }

    .header {
        animation: slideIn 1s ease-in-out;
        font-size: 1.5rem;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 10px;
    }

    .chat-history {
        margin-bottom: 10px;
        max-height: 60vh;
        overflow-y: auto;
    }

    .input-box {
        width: 100%;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ccc;
        margin-bottom: 10px;
    }

    .button {
        width: 100%;
        animation: fadeIn 1s ease-in-out;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.3s ease;
        border-radius: 5px;
    }
    
    .button:hover {
        background-color: #45a049;
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# HTML structure for the chat interface
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
st.markdown('<div class="header">Stress Management Q&A</div>', unsafe_allow_html=True)

# Chat history container
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for chat in st.session_state.chat_history:
    st.markdown(f'<div class="chat-history">{chat}</div>', unsafe_allow_html=True)

# Streamlit input and button setup using standard Streamlit widgets
input_text = st.text_input("", key="input", placeholder="Type your question here...")
submit = st.button("Get Advice", key="submit")

def get_response(question):
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )
    completion = client.chat.completions.create(
        model="mistralai/mistral-large",
        messages=[{"role": "user", "content": question}],
        temperature=0.0,
        top_p=1,
        max_tokens=512,
        stream=True
    )
    response_text = ""
    for chunk in completion:
        response_text += chunk.choices[0].delta.content

    return response_text

# Handle button click
if submit:
    if input_text:
        st.session_state.chat_history.append(f"You: {input_text}")
        response = get_response(input_text)
        st.session_state.chat_history.append(f"Bot: {response}")
        
        # Instead of using st.experimental_rerun(), we clear the input field manually
        st.query_params()
    else:
        st.error("Please enter a question about stress.")

st.markdown('</div>', unsafe_allow_html=True)
