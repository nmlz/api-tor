import requests
import pymongo

client = pymongo.MongoClient('mongodb+srv://nmlz:0QR9rTgFaAXMEHIURhYv@cluster0.8vngv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
mydb = client["tor_ips"]
mycol_full = mydb["full"] #Collection completa

def drop(): #Borra la collection/tabla para cargar los nuevos request y evitar repetidos
    mycol_full.drop()

def req_dan():
    url_data_dan = requests.get("https://www.dan.me.uk/torlist/?exit")
    if url_data_dan.status_code != 200:
        return "Conexión Fallida"
    else:
        url_dan = url_data_dan.content.decode().split('\n')
        url_dan_list = []
        for i in url_dan:
            url_dan_list.append({"ip":i, "exclusion":False})
        mycol_full.insert_many(url_dan_list, ordered = False)


def req_bdc():
    url_data_bdc = requests.get("https://api.bigdatacloud.net/data/tor-exit-nodes-list?batchSize=1000&offset=0&localityLanguage=es&key=84a06ef229604e3dbd785fa60b407788")
    if url_data_bdc.status_code != 200:
        return "Conexión Fallida"
    else:
        url_bdc_list = []
        for i in url_data_bdc.json()["nodes"]:
            url_bdc_list.append({"ip":i["ip"], "exclusion": False})
        mycol_full.insert_many(url_bdc_list, ordered = False)

def lambda_handler(event, context):
    # drop()
    req_dan()
    req_bdc()