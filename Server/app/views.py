from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/model', methods=['POST'])
def MakeResponse():
    input = request.json
    text = input.get('text')
    return make_response(jsonify({"response": mock_model(text)}), 200)
    

def mock_model(text):
    return f"hello, {text}"