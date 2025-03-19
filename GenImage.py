import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64

# Cấu hình API
client = genai.Client(api_key='AIzaSyApnSpZVliqfTKmhfEOu66kczAbsvyPslQ')

def generate_image(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['Text', 'Image']
            )
        )

        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data is not None:
                image_data = part.inline_data.data
                image = Image.open(BytesIO(image_data))
                image.save('gemini-native-image.png')
                image.show()

    except Exception as e:
        print(f"An error occurred: {e}")

# Giao diện Streamlit
st.title("Gemini Image Generator")
prompt = st.text_input("Enter a prompt for image generation:")

if st.button("Generate Image"):
    if prompt:
        image = generate_image(prompt)
        if image:
            st.image(image, caption="Generated Image", use_column_width=True)
    else:
        st.warning("Please enter a prompt!")
