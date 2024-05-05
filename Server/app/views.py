from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from openai import OpenAI
import pdfplumber
import os

app = Flask(__name__)
CORS(app)

@app.route('/model', methods=['POST'])
def MakeResponse():
    input = request.json
    text = input.get('text')
    return make_response(jsonify({"response": create_response(text)}), 200)
    

def create_response(input_query):
    query = input_query
    client = OpenAI(api_key="")
    pdf_path = os.path.join(os.getcwd(), "app/Asperger.pdf")
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    chunks = [text[i:i + 1000] for i in range(0, len(text), 1000)]
    context = "\n\n".join(chunks[:2])

    messages = [
        {"role": "system", "content": "You are a helpful assistant using PDF resources."},
        {"role": "user", "content": query},
        {"role": "system", "content": f"PDF Context: {context}"}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return response.choices[0].message.content