import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_text_from_image(image_path):
    model = genai.GenerativeModel("gemini-pro-vision")
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    response = model.generate_content([image_data])
    return response.text if response else ""