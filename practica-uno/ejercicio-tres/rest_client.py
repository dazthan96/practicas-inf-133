import requests
url = "http://localhost:8000/"
ruta_get = url +"/pacientes"
get_response = requests.request(method="GET",url=ruta_get)
print(get_response.text)
print("<------------------------------------>")
print("<----------------------crear paciente>")
ruta_post =url+"pacientes"
nuevo_paciente = {
    "ci":222222,
    "nombre":"pedro",
    "apellido":"sanchez",
    "edad":30,
    "genero":"masculino",
    "diagnostico":"Diabetes",
    "doctor":"manuel_callejas"
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_paciente)
print(post_response.text)

print("<------------------------------------>")
print("<------------------listando pacientes>")
get_response = requests.request(method="GET",url=ruta_get)
print(get_response.text)

print("<------------------------------------>")
print("<-------------buscar pacientes por ci>")
ruta_get_ci = url+"pacientes/222222"
response_get_ci=requests.request(method="GET", url=ruta_get_ci)
print(response_get_ci.text)

print("<------------------------------------>")
print("<---------buscar pacientes por doctor>")
ruta_get_doc = url +"pacientes?doctor=mauricio_peredo"
response_get_doctor = requests.request(method="GET", url=ruta_get_doc)
print(response_get_doctor.text)

print("<------------------------------------>")
print("<-----------------actualizar paciente>")
paciente_actualizar ={
    "nombre":"pablo",
    "apellido":"marmol",
    "edad":50,
    "genero":"masculino",
    "diagnostico":"artritis",
    "doctor":"mauricio_peredo"
}
ruta_put_actualizar=url +"pacientes/111111"
response_put_actualizar = requests.request(method="PUT", url=ruta_put_actualizar,json=paciente_actualizar)
print(response_put_actualizar.text)

print("<------------------------------------>")
print("<-------------------eliminando paciente...>")
ruta_delete_paciente = url+"pacientes/111111"
response_delete_paciente = requests.request(method="DELETE", url=ruta_delete_paciente)
print(response_delete_paciente.text)

print("<------------------listando pacientes>")
get_response = requests.request(method="GET",url=ruta_get)
print(get_response.text)
