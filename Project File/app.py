from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

load_dotenv()  # Load variables from .env file

# Securely fetch API key
api_key = os.getenv("GOOGLE_API_KEY")

# Check if API key exists
if not api_key:
    st.error("⚠️ API Key not found. Please check your .env file.")
else:
    genai.configure(api_key=api_key)

# --- 2. Function to Get Gemini Response ---
def get_gemini_response(input_text, image, prompt):
  model = genai.GenerativeModel("gemini-2.5-flash")
  response = model.generate_content([input_text, image[0], prompt])
  return response.text
    # --- 3. Function to Setup Input Image ---
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # e.g., 'image/jpeg' or 'image/png'
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# --- 4. Streamlit UI Layout ---
st.set_page_config(page_title="Gemini Historical Artifact Description App", page_icon="🏺")

st.header("🏺 Gemini Historical Artifact Description App")

# Input fields
input_text = st.text_input("📝 Input Prompt (Optional):", key="input")
uploaded_file = st.file_uploader("🖼️ Choose an image of an artifact...", type=["jpg", "jpeg", "png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("🚀 Generate Artifact Description")

# --- 5. System Prompt (The "Historian" Persona) ---
input_prompt = """
You are an expert historian and archaeologist. 
Please examine the uploaded image of the historical artifact carefully.
Provide a detailed description including:
1. The likely Name of the artifact.
2. Its Origin and Time Period.
3. The Materials used and craftsmanship details.
4. Its Historical and Cultural Significance.
5. Any interesting facts or stories associated with it.
"""

# --- 6. Execution Logic ---
if submit:
    if uploaded_file is None:
        st.warning("Please upload an image first.")
    else:
        try:
            with st.spinner("Analyzing history..."):
                # Process the image
                image_data = input_image_setup(uploaded_file)
                # Call the AI model
                response = get_gemini_response(input_text, image_data, input_prompt)
                
                # Display results
                st.subheader("📜 Description of the Artifact:")
                st.write(response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
