from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

def sumar (num1, num2):
    return num1+num2

def resta(num1, num2):
    return num1-num2

def multiplicacion(num1,num2):
    return num1*num2
def division(num1, num2):
    if num2==0:
        return "no se puede dividir"
    else:
        return str(num1/num2)
        
dispatcher = SoapDispatcher(
    "practica-1-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)

dispatcher.register_function(
    "Sumar",
    sumar,
    returns={"resultado":int},
    args={"num1":int,"num2":int},
)
dispatcher.register_function(
    "Resta",
    resta,
    returns={"resultado":int},
    args={"num1":int,"num2":int},
)
dispatcher.register_function(
    "Multiplicacion",
    multiplicacion,
    returns={"resultado":int},
    args={"num1":int,"num2":int}
)
dispatcher.register_function(
    "Division",
    division,
    returns={"resultado":str},
    args={"num1":int,"num2":int},
)
server = HTTPServer(("0.0.0.0",8000), SOAPHandler)
server.dispatcher = dispatcher
print("servidor SOAP iniciado e http://localhost:8000/")
server.serve_forever()