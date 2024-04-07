import requests
url = 'http://localhost:8000/graphql'
print("<------------------------creando planta>")
query_crear = """
mutation {
    crearPlantas(nombre:"planta nueva",especie:"suculenta",edad:55,altura:555, frutos:False){
        planta {
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
}
"""
response_crear = requests.post(url, json ={'query':query_crear})
print(response_crear.text)
print("<-------------------------------------->")
print("<----------------------listando plantas>")
query_lista = """
{
        plantas{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }    
"""

#solicitud POST al servidor Graphql

response = requests.post(url, json={'query':query_lista})
print(response.text)
print("<-------------------------------------->")
print("<-------------------plantas por especie>")
query_especie="""
    {
        plantaPorEspecie(especie:"arbol"){
            id
            nombre
            especie
        }        
    }
"""

response_plantas_especie = requests.post(url, json={'query':query_especie})
print(response_plantas_especie.text)
print("<-------------------------------------->")
print("<--------------------plantas por frutos>")
query_fruto="""
    {
        plantaPorFruto{
            nombre
            frutos
        }
    }
"""
response_planta_fruto = requests.post(url, json = {'query':query_fruto})
print(response_planta_fruto.text)
print("<-------------------------------------->")
print("<---------------------eliminando planta>")
query_delete ="""
mutation{
        deletePlanta(id:2){
            planta {
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""
response_mutation = requests.post(url, json ={'query':query_delete})
print(response_mutation.text)
print("<-------------------------------------->")
print("<-------------------actualizando planta>")

query_actualizar = """
mutation{
    actualizarPlanta(id:3, nombre:"planta4",especie:"especie4", edad:4,altura:4, frutos:True){
        planta {
            id
            nombre
            especie
            edad
            altura
            frutos
        } 
    }
}
"""
response_actualizar = requests.post(url, json = {'query':query_actualizar})
print(response_actualizar.text)
print("<-------------------------------------->")
response = requests.post(url,json={'query':query_lista})
print(response.text)
#\"""
#    Construye un API con GraphQL para gestionar el seguimiento de las plantas de un vivero. La API debe permitir:
#    - Crear una planta
#    - Listar todas las plantas
#    - Buscar plantas por especie
#    - Buscar las plantas que tienen frutos
#    - Actualizar la información de una planta
#    - Eliminar una planta
#
#    De las plantas se debe almacenar la siguiente información:
#    - ID (identificador único)
#    - Nombre común (nombre popular)
#    - Especie (nombre científico)
#    - Edad (en meses)
#    - Altura (en cm)
#    - Frutos (booleano)
#
#  **Rutas esperadas:**
#   - `/graphql`
