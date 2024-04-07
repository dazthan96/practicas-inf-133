import requests
url = "http://localhost:8000/"
ruta_get = url +"/animales"
get_response = requests.request(method="GET",url=ruta_get)
print(get_response.text)
print("<------------------------------------>")
print("<----------------------crear animal>")
ruta_post =url+"animales"
nuevo_animal = {
    "id":2,
    "nombre":"shifu",
    "especie":"sarihulla",
    "genero":"macho",
    "edad":2,
    "peso":1
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_animal)
print(post_response.text)

print("<------------------------------------>")
print("<------------------listando animales>")
listando_animales = requests.request(method="GET",url=ruta_get)
print(listando_animales.text)

print("<------------------------------------>")
print("<---------buscar animales por especie>")
ruta_get_especie = url +"animales?especie=sarihulla"
response_get_especie = requests.request(method="GET",url=ruta_get_especie)
print(response_get_especie.text)

print("<------------------------------------>")
print("<----------buscar animales por genero>")
ruta_get_genero = url +"animales?genero=hembra"
response_get_genero = requests.request(method="GET",url=ruta_get_genero)
print(response_get_genero.text)

print("<------------------------------------>")
print("<-------------------actualizar animal>")

actualizar_animal = {
    "nombre":"animal_actualizado",
    "especie":"especie_Actualizada",
    "genero":"macho",
    "edad":4,
    "peso":2
}
ruta_put = url +"animales/2"
response_put = requests.request(method="PUT",url=ruta_put,json=actualizar_animal)
print(response_put.text)

print("<------------------------------------>")
print("<-------------------eliminando paciente...>")
ruta_delete =url +"animales/1"
response_delete = requests.request(method="DELETE", url=ruta_delete)
print(response_delete.text)

print("<------------------listando animales>")
get_response=requests.request(method="GET", url=ruta_get)
print(get_response.text)
