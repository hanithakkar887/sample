import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')

# Set up Streamlit app
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #2e2e2e;  /* Dark background color */
        color: #e0e0e0;  /* Light text color */
        font-family: 'Courier New', Courier, monospace;  /* Custom font */
    }
    .title {
        color: #FFD700;  /* Gold color for title */
        font-size: 3em;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
        font-family: 'Georgia', serif;
    }
    .input-box {
        background-color: #1c1c1c;  /* Darker input box background */
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        color: #e0e0e0;
        font-size: 1.2em;
    }
    .button {
        background-color: #00BFFF;  /* Deep Sky Blue color for button */
        color: sky;
        font-size: 1.2em;
        border-radius: 8px;
        padding: 10px 20px;
        cursor: pointer;
    }
    .button:hover {
        background-color: #4682B4;  /* Steel Blue color on hover */
    }
    .response-box {
        background-color: #2F4F4F;  /* Dark Slate Gray background */
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        font-size: 1.5em;
        color: #FFD700;  /* Gold text color */
        font-family: 'Georgia', serif;
    }
    .footer {
        margin-top: 50px;
        text-align: center;
        font-size: 0.8em;
        color: #a0a0a0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown('<h1 class="title">AI Assistant</h1>', unsafe_allow_html=True)

# Input box for user query
user_input = st.text_input("Ask me anything:", key="query", help="Type your question or input here.", max_chars=1000)

# Button to generate response
if st.button("Get Response", key="generate", help="Click to get a response from the AI"):
    if not api_key:
        st.markdown('<p class="warning">API key not found. Please set it as an environment variable or in the .env file.</p>', unsafe_allow_html=True)
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        try:
            prompt = f"Respond to the following query: {user_input}"
            response = model.generate_content(prompt)
            
            if response and hasattr(response, 'candidates') and response.candidates:
                generated_response = ""
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and candidate.content.parts:
                        for part in candidate.content.parts:
                            if hasattr(part, 'text'):
                                generated_response += part.text + "\n"
                            else:
                                st.markdown('<p class="warning">No text found in this part.</p>', unsafe_allow_html=True)
                    else:
                        st.markdown('<p class="warning">No content found in this candidate.</p>', unsafe_allow_html=True)
                
                if generated_response:
                    st.markdown('<div class="response-box">Response:</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="response-box">{generated_response}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<p class="warning">No valid candidates found in the response.</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="warning">No valid candidates found in the response.</p>', unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<p class="warning">An error occurred: {e}</p>', unsafe_allow_html=True)

# Instructions with styling
st.markdown("""
## Instructions
1. **Type your question or input** in the text input box above.
2. **Click the "Get Response" button** to get a response from the AI.
3. The **response** will be displayed below.
""")

# Footer
st.markdown('<div class="footer">Powered by Google Generative AI | Designed with ❤️ by Hani Thakkar</div>', unsafe_allow_html=True)


# luma,sora,groq,sombanova,runway,gen3alpha,luma,elevenbales with sora,searchgpt,perplacityai,