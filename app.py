from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from image_recognition import recognize_image
from chatbot import generate_response1
from chat import chatbot_response
app = Flask(__name__)


os.makedirs('uploads', exist_ok=True)


@app.route('/')
def index():
    return render_template('index3.html')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get("message")

    if not text:
        return jsonify({"answer": "Please provide a message."})  # Return an error if no message is provided

    response = chatbot_response(text)  # Get the GPT-2 based response
    return jsonify({"answer": response})  # Return the response as JSON


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files['image']
    filename = secure_filename(image_file.filename)
    filepath = os.path.join('uploads', filename)
    image_file.save(filepath)

    # Recognize the image content
    recognized_objects = recognize_image(filepath)
    image_description = ", ".join([f"{obj[0]} ({obj[1] * 100:.2f}%)" for obj in recognized_objects])

    # Generate GPT-2 based response based on image description
    chatbot_response = generate_response1(image_description)

    return jsonify({"response": chatbot_response, "description": image_description})


if __name__ == '__main__':
    app.run(debug=True)