import requests
url = "http://localhost:8000/"
headers={"Content-type":"application/json"}

print("<------------------------------------>")
print("<----------------------crear paciente>")

nuevo_paciente = {
    "ci":222222,
    "nombre":"pedro",
    "apellido":"sanchez",
    "edad":30,
    "genero":"masculino",
    "diagnostico":"Diabetes",
    "doctor":"manuel_callejas"
}
url_post=url+"pacientes"
response = requests.post(url_post, json=nuevo_paciente, headers=headers)
print(response.json())

print("<------------------------------------>")
print("<------------------listando pacientes>")
url_lista_pacientes=url+"pacientes"
response_lista = requests.get(url_lista_pacientes, headers=headers)
print(response_lista.text)

print("<------------------------------------>")
print("<-------------buscar pacientes por ci>")
url_paciente_ci=url+"pacientes/111111"
response_paciente_ci=requests.get(url=url_paciente_ci,headers=headers)
print(response_paciente_ci.text)

print("<------------------------------------>")
print("<---------buscar pacientes por doctor>")
url_paciente_doctor=url+"pacientes?doctor=mauricio_peredo"
response_paciente_doctor=requests.get(url=url_paciente_doctor,headers=headers)
print(response_paciente_doctor.text)


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
response_put_actualizar = requests.put(url=ruta_put_actualizar,json=paciente_actualizar,headers=headers)
print(response_put_actualizar.text)


print("<------------------------------------>")
print("<-------------------eliminando paciente...>")
url_delete_paciente=url+"pacientes/111111"
response_delete_paciente=requests.delete(url=url_delete_paciente, headers=headers)
print(response_delete_paciente.text)

print("<------------------listando pacientes>")
get_response = requests.get(url=url_lista_pacientes,headers=headers)
print(get_response.text)