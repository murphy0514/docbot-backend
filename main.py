from flask import Flask, request, jsonify
import openai
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

@app.route("/analyze", methods=["POST"])
def analyze():
    if 'file' not in request.files or 'query' not in request.form:
        return jsonify({"error": "Missing file or query"}), 400

    file = request.files['file']
    query = request.form['query']
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    with open(file_path, "rb") as f:
        extracted_text = extract_text_from_pdf(f)

    prompt = f"""
You are a professional document analysis assistant for a Canadian law firm.

A user uploaded this document:
"""
{extracted_text}
"""

They asked: "{query}"

Your task is to generate a structured, professional response with bullet points or tables if needed. Always use Canadian dollars. Keep the tone factual and legal.
"""
response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    result_text = response['choices'][0]['message']['content']
    return jsonify({"report": result_text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
