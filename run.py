import streamlit as st
import requests
from io import BytesIO
from PIL import Image

# Assuming you have your DeepSeek API key stored as an environment variable
DEEPSEEK_API_KEY = st.secrets["DEEPSEEK_API_KEY"]
DEEPSEEK_API_URL = "YOUR_DEEPSEEK_API_ENDPOINT_HERE"

def describe_image(image, prompt):
    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }
    # Convert image to bytes for sending
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    data = {
        "prompt": prompt,
        "image": img_byte_arr
    }
    
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json().get('description', "No description provided")
    else:
        return f"Error: {response.status_code} - {response.text}"

def main():
    st.title("Strike Zone Analysis")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        
        if st.button('Describe'):
            with st.spinner('Describing image...'):
                description = describe_image(image, "describe the image")
                st.write(description)

if __name__ == "__main__":
    main()