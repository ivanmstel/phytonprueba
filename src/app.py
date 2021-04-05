#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Ivan
#
# Created:     26/03/2021
# Copyright:   (c) Ivan 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# importamos los modulos necesarios
# modulos de flask
from flask import Flask, request, jsonify
# modulos  del orm
from flask_sqlalchemy import SQLAlchemy
# modulo para facilitar los parseos
from flask_marshmallow import Marshmallow
#------------------------------------------------------------------------------

app = Flask(__name__)
# conexión con la base de datos: tipo+driver://usuario:clave@ip/bd
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://ecdvarvbesstqr:48a7bbd45cc1154b1f8067f8a4e179796115aad4a90be2fa2ff152563629feaa@ec2-52-50-171-4.eu-west-1.compute.amazonaws.com:5432/d4v2asm6smqvgk'
#con este evitamos warinigs
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#instancia de la base de datos a través del orm
db = SQLAlchemy(app)
# instancia de marshmallow para generar esqueams y facilitar el parseo
ma = Marshmallow(app)

#------------------------------------------------------------------------------
#creación de los modelos de las diferentes tablas
class Provincias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))


    def __init__(self,nombre):
        self.nombre = nombre


# si no ecisten las tabla se crearía con
#db.create_all()

# ahora definimos un schema con el que podremos interacturar e indicar los
#campos que queremos obtener
class ProvinciasSchema(ma.Schema):
    class Meta:
        fields=('id','nombre')

#ahora realizamos dos instanciaciones, una para cuando recibamos un único elemento
# y otra para listas de elementos

provincia_schema= ProvinciasSchema()
# y ahora para varios poniendo la propiedad many a true
provincias_schema=ProvinciasSchema(many=True)

#-------------------------------------------------------------------------
#implementación de los métodos CRUD


@app.route('/provincias/insertar', methods=['POST'])
def insertar_provincia():
  nombre = request.json['nombre']


  nueva_provincia= Provincias(nombre)

  db.session.add(nueva_provincia)
  db.session.commit()

  return provincia_schema.jsonify(nueva_provincia)

@app.route('/provincias/todas', methods=['GET'])
def get_provincias():
  todas_provincias = Provincias.query.all()
  result = provincias_schema.dump(todas_provincias)
  return jsonify(result)

@app.route('/provincia/<id>', methods=['GET'])
def get_provincia(id):
  provincia = Provincias.query.get(id)
  return provincia_schema.jsonify(provincia)

@app.route('/provincia/<id>', methods=['PUT'])
def actualizar_provincia(id):
  provincia = Provincias.query.get(id)

  nombre = request.json['nombre']
  provincia.nombre = nombre
  db.session.commit()

  return provincia_schema.jsonify(provincia)

@app.route('/provincia/<id>', methods=['DELETE'])
def borrar_provincia(id):
  provincia = Provincias.query.get(id)
  db.session.delete(provincia)
  db.session.commit()
  return provincia_schema.jsonify(provincia)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to my API'})


#lanza la aplicación en modo debug de forma que se reinicia tras cambios
if __name__ == "__main__":
    app.run(debug=True)