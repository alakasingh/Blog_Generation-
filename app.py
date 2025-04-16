import streamlit as st
import requests

# Hugging Face Inference API details
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
headers = {"Authorization": "Bearer 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"}

# Function to get response from Flan-T5 model
def getFlanResponse(input_text, no_words, blog_style):
    try:
        max_tokens = min(int(no_words) * 2, 250)  # Clamp to max 250 tokens
    except ValueError:
        return "Please enter a valid number of words."

    # Prompt template
    template = """
    Write a blog post suitable for a {} on the topic "{}". Limit it to approximately {} words. Make it clear, engaging, and informative.
    """
    prompt = template.format(blog_style, input_text, no_words)

    # Send request to Hugging Face API
    response = requests.post(API_URL, headers=headers, json={
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 0.9
        }
    })

    # Return generated text or error
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit UI setup
st.set_page_config(page_title="Generate Blogs 🤖",
                   page_icon='📝', 
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("Generate Blogs 🤖")

# User input fields
input_text = st.text_input("Enter the Blog Topic")

col1, col2 = st.columns(2)
with col1:
    no_words = st.text_input("No of Words")
with col2:
    blog_style = st.selectbox("Writing the Blog for", 
                              ['Researcher', 'Data Scientist', 'Common People'])

# Generate button
submit = st.button("Generate")

# Generate and display blog
if submit:
    if input_text and no_words:
        result = getFlanResponse(input_text, no_words, blog_style)
        st.markdown("### ✍️ Generated Blog")
        st.write(result)
    else:
        st.warning("Please fill in all fields.")
