import streamlit as st
import requests

API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
headers = {"Authorization": "Bearer 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"}

from langchain import PromptTemplate


# Function to create response from Llama model
def getLlamaResponse(input_text, no_words, blog_style):
    # Prompt TEMPLATE
    template = """
    Write a blog for {} job profile for a topic "{}" within {} words.
    """
    
    # Creating the prompt using the provided input
    prompt = template.format(blog_style, input_text, no_words)
    
    # Sending the prompt to the Hugging Face API
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    
    # Check if the response is successful
    if response.status_code == 200:
        # Parse and return the response text from the model
        return response.json()[0]["generated_text"]
    else:
        return f"Error: {response.status_code} - {response.text}"


st.set_page_config(page_title="Generate Blogs",
                   page_icon='🤖', 
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("Generate Blogs 🤖")

input_text = st.text_input("Enter the Blog Topic")

# Creating two more columns for additional fields
col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('No of Words')
with col2:
    blog_style = st.selectbox('Writing the Blog for', ('Researcher', 'Data Scientist', 'Common People'), index=0)

submit = st.button("Generate")

# Final Response
if submit:
    if input_text and no_words:
        response = getLlamaResponse(input_text, no_words, blog_style)
        st.write(response)
    else:
        st.write("Please fill in all fields.")
