from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

@app.route('/')
def index():
    titulo = "IEVN-1001"
    list = ["Miguel", "Juan", "Pedro", "Luis"]
    return render_template('uno.html',titulo=titulo, list=list)

""" @app.route('/user/<string:user>')
def user(user):
    return "El usuario es: {}".format(user)

@app.route('/user/<int:n1>')
def numero(n1):
    return "El numero es: {}".format(n1)

@app.route('/user/<string:user>/<int:id>')
def user(user, id):
    return "<h1>El usuario es: {} y su id es: {}</h1>".format(user, id)

@app.route('/suma/<int:n1>/<int:n2>')
def suma(n1, n2):
    return "<h1>La suma de {} y {} es: {}</h1>".format(n1, n2, n1+n2)

@app.route('/default')

@app.route('/default/<string:nombre>')
def nom2(nom='Miguel'):
    return "<h1>El nombre es: {}</h1>".format(nom) """

if __name__ == '__main__':
    app.run(debug=True)