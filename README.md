# TOR
API Rest

## Endpoints
### [GET] /
Indica endpoints de la API
### [GET] /list
Lista IPs recibidas de:

● https://www.dan.me.uk/tornodes

● https://www.bigdatacloud.com/insights/tor-exit-nodes
### [POST] /exclusion
Endpoint POST para cargar IP a excluir 

(Ejemplo de como enviarlo vía Postman:

https://user-images.githubusercontent.com/79547083/144382814-8c7300fb-cb26-4209-b14e-2a4e94acc52e.png)

### [GET] /customlist
Lista sin IPs excluidas

## Realizado con:
**Framework** - **Flask**

**DB** - **MongoDB**

**Librerias** - **PyMongo**

**Container** - **Docker**

**Cloud** - **AWS**
Acceder vía:

http://ec2-3-142-114-40.us-east-2.compute.amazonaws.com:5000/ NO LEVANTADO ACTUALMENTE

**main.py es la Lambda function**
