from flask import Flask, jsonify, request
import traceback
import json
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb+srv://nmlz:0QR9rTgFaAXMEHIURhYv@cluster0.8vngv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
mydb = client["tor_ips"]
mycol = mydb["ips"] #Collection completa
mycol_full = mydb["full"] #Collection con POST de usuario    

@app.route("/")
def endpoints():
    try:
        # Print endpoints disponibles
        result = "<h1>RestAPI TOR MeLi</h1>"
        result += "<h2>Endpoints disponibles:</h2>"
        result += "<h3>[GET] /list --> Listado de nodos de salida de TOR</h3>"
        result += "<h3>[POST] /exclusion --> Ingresar ip a excluir de listado de nodos de salida de TOR</h3>"
        result += "<h3>[GET] /customlist --> Listado de nodos de salida de TOR exceptuando exclusiones indicadas</h3>"
        return(result)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/list")
def index():
    x = []
    for i in mycol_full.find():
        x.append(i['ip'])
    return json.dumps({"ips":x}) 


@app.route("/exclusion", methods = ['POST'])
def exclusion():
    ips = request.json['ip']
    query = {"ip":ips}
    newvalues = {"$set":{"exclusion":True}}
    mycol_full.update_one(query, newvalues) #Actualiza el valor de exclusion a True si encuentra la ip guardada en query
    mycol.insert_one({"ip":ips}) #Guarda la IP dentro de la collection ips.

    return "IP Cargada"
    

@app.route("/customlist")
def customlist():
    x = []
    for i in mycol_full.find({"exclusion":False}):
        x.append(i['ip'])
    return json.dumps({"ips":x}) #Devolvemos todas las ips excepto las excluidas por POST
    
    
if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0"
    )
