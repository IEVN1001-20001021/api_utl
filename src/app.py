from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

con = MySQL(app)

@app.route('/alumnos', methods=['GET'])
def lista_alumnos():
    try:
        cursor = con.connection.cursor()
        sql="SELECT * FROM alumnos"
        cursor.execute(sql)
        datos = cursor.fetchall()
        alumnos = []
        for fila in datos:
            alumno = {
                'id': fila[0],
                'nombre': fila[1],
                'apellido': fila[2],
                'email': fila[3]
            }
            alumnos.append(alumno)
        return jsonify({'alumnos': alumnos, 'mensaje': 'Lista de alumnos'}), 200
    except Exception as ex:
        return jsonify({"message": "error{}".format(ex), "exito": False}), 500
    return ''

def leer_alumno_bd(matricula):
    try:
        cursor = con.connection.cursor()
        sql = "SELECT * FROM alumnos WHERE matricula = {}".format(matricula)
        cursor.execute(sql)
        datos = cursor.fetchone()
       
        if datos != None:
            alumno = {'matricula': datos[0], 'nombre': datos[1], 'apaterno': datos[2], 'amaterno': datos[3], 'correo': datos[4]}
            return alumno
        else:
            return None
    except Exception as ex:
        raise ex
 
 
@app.route("/alumnos/<mat>", methods=['GET'])
def leer_alumno(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno != None:
            return jsonify({'alumno': alumno, 'mensaje': 'Alumno encontrado', 'exito': True})
        else:
            return jsonify({'alumno': None, 'mensaje': 'Alumno no encontrado', 'exito': False})
    except Exception as ex:
        return jsonify({"message": "error {}".format(ex), 'exito': False}), 500
    
@app.route('/alumnos', methods=['POST'])
def registrar_alumno():
    required_fields = ['matricula', 'nombre', 'apaterno', 'amaterno', 'correo']
    data = request.json

    # Validar que todos los campos requeridos están presentes
    for field in required_fields:
        if field not in data:
            return jsonify({'mensaje': f'Falta el campo {field}', 'exito': False}), 400

    try:
        alumno = leer_alumno_bd(data['matricula'])
        if alumno is not None:
            return jsonify({'mensaje': 'Alumno ya existe', 'exito': False}), 400
        else:
            cursor = con.connection.cursor()
            sql = "INSERT INTO alumnos (matricula, nombre, apaterno, amaterno, correo) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (data['matricula'], data['nombre'], data['apaterno'], data['amaterno'], data['correo']))
            con.connection.commit()
            return jsonify({'mensaje': 'Alumno registrado', 'exito': True}), 201
    except Exception as ex:
        return jsonify({'mensaje': f'Error {ex}', 'exito': False}), 500

def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(400, pagina_no_encontrada)
    app.run(host='0.0.0.0', port=5000)