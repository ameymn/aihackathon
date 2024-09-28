from flask import Flask, request, jsonify
from PIL import Image
# import pytesseract
import google.generativeai as genai
import os

app = Flask(__name__)

# Set up your Google Generative AI model
model = genai.GenerativeModel(model_name='gemini-1.5-pro-latest')

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/extract_text', methods=['POST'])
def extract_text():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        image_file = request.files['image']
        
        # Open the image using PIL
        img = Image.open(image_file)
        
        # Use Google Generative AI to extract text
        prompt = "Give me the text in the image in json format"
        response = model.generate_content([prompt, img])
        
        # Return the extracted text as JSON
        return jsonify({"extracted_text": response.text})
    except Exception as e:
        # Log the full exception traceback
        app.logger.error(f"An error occurred: {str(e)}\n{traceback.format_exc()}")
        
        # Return a detailed error response
        return jsonify({
            "error": "An error occurred while processing the request",
            "details": str(e),
            "route": "/extract_text",
            "method": "POST"
        }), 500
    

if __name__ == '__main__':
    app.run(debug=True)