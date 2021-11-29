from flask import Flask, jsonify, request
import traceback
import requests
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
    url_data_bdc = requests.get("https://api.bigdatacloud.net/data/tor-exit-nodes-list?batchSize=1000&offset=0&localityLanguage=es&key=84a06ef229604e3dbd785fa60b407788")
    if url_data_bdc.status_code != 200:
        return "Conexión Fallida"
    else:
        data_bdc = json.loads(url_data_bdc.content)
        for i in data_bdc["nodes"]: 
            i["exclusion"] = False #Agrega una nueva key llamada exclusion con value False a todo el json recibido del request
        ip_list_bdc = []
        for datos in data_bdc["nodes"]:
            ip_list_bdc.append(datos['ip'])
        ip_json = json.dumps(ip_list_bdc, sort_keys=True, indent=4)
        mycol_full.insert_many(data_bdc["nodes"]) #Inserta el json modificado con la nueva key a nuestra db
        return ip_json


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
    app.run(debug=True
    )




# https://www.dan.me.uk/torlist/?exit