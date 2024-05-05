from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Estás en la página de inicio.'

@app.route('/saludo')
def hello_world():
    return 'Hello, World!'

@app.route('/saludo-personalizado', methods=['POST'])
def saludo_personalizado():
    data = request.json
    nombre = data.get('nombre', 'Invitado')
    return f'Hola, {nombre}!'