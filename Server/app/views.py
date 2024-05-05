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
    
client = OpenAI(api_key="")

historial = []
def create_response(input_query):
    pdf_path = os.path.join(os.getcwd(), "app\\\\Asperger.pdf")
    
    # Cargar el contenido del PDF
    with pdfplumber.open(pdf_path) as pdf:
        texto = "".join(page.extract_text() for page in pdf.pages)

    # Crear contexto desde el historial
    contexto_historial = "\n\n".join(historial[-5:])  # Usamos las últimas 5 interacciones como contexto

    # Añadir el nuevo input a la memoria
    historial.append(f"Usuario: {input_query}")

    # Crear la lista de mensajes
    mensajes = [
        {"role": "system", "content": "You are a helpful assistant using PDF resources."},
        {"role": "system", "content": f"Historial: {contexto_historial}"},
        {"role": "user", "content": input_query},
        {"role": "system", "content": f"PDF Context: {texto[:1000]}"}
    ]

    # Generar respuesta con el modelo
    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=mensajes
    )

    # Guardar la respuesta generada en el historial
    historial.append(f"Asistente: {respuesta.choices[0].message.content}")

    return respuesta.choices[0].message.content