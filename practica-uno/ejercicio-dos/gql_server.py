from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, Boolean, List, Schema, Field, Mutation

class Planta(ObjectType):
    id = Int()
    nombre = String()
    especie =String()
    edad = Int()
    altura = Int()
    frutos = Boolean()


class Query(ObjectType):
    plantas = List(Planta)
    planta_por_id = Field(Planta, id=Int())
    planta_por_especie = List(Planta, especie=String())
    planta_por_fruto = List(Planta)
    
    def resolve_plantas(root, info):
        return plantas
    
    def resolve_planta_por_id(root, info, id):
        for planta in plantas:
            if planta.id == id:
                return planta
        return None
    
    def resolve_planta_por_especie(root, info, especie):
        plantas_especie = []
        for planta in plantas:
            if planta.especie == especie:
                plantas_especie.append(planta)
        return plantas_especie
    
    def resolve_planta_por_fruto(root, info):
        planta_fruto=[]
        for planta in plantas:
            if planta.frutos==True:
                planta_fruto.append(planta)
        return planta_fruto

    
class CrearPlantas(Mutation):
    class Arguments:
        nombre = String()
        especie = String()
        edad = Int()
        altura = Int()
        frutos = Boolean()
    
    planta = Field(Planta)
    
    def mutate(root, info, nombre, especie, edad, altura, frutos):
        nueva_planta = Planta(
            id=len(plantas)+1,
            nombre=nombre,
            especie=especie,
            edad=edad,
            altura=altura,
            frutos=frutos
            )
        plantas.append(nueva_planta)
        return CrearPlantas(planta=nueva_planta)
    
class DeletePlanta(Mutation):
    class Arguments:
        id = Int()
    
    planta = Field(Planta)
    
    def mutate(root, info, id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return DeletePlanta(planta = planta)
        return None

class ActualizarPlanta(Mutation):
    class Arguments:
        id = Int()
        nombre = String()
        especie = String()
        edad = Int()
        altura = Int()
        frutos = Boolean()
    
    planta = Field(Planta)
    
    def mutate(root, info, id, nombre, especie, edad, altura, frutos):
        for planta in plantas:
            if planta.id == id:
                planta.nombre = nombre
                planta.especie = especie
                planta.edad = edad
                planta.altura = altura
                planta.frutos = frutos
                return ActualizarPlanta(planta=planta)
        return None

class Mutations(ObjectType):
    crear_planta = CrearPlantas.Field()
    delete_planta = DeletePlanta.Field()
    actualizar_planta = ActualizarPlanta.Field()

plantas = [
    Planta(
        id=1, nombre="planta-uno", especie="arbol", edad=11, altura=111, frutos=False
    ),
    Planta(id=2, nombre="planta-dos", especie="arbol", edad=22,altura=222, frutos=True),
    Planta(
        id=3, nombre="planta-tres", especie="suculenta", edad=33, altura=333, frutos=True
    ),
    Planta(
        id=4, nombre="planta-cuatro", especie="cactus", edad=44, altura=444, frutos=False
    ),
]

schema = Schema(query=Query, mutation=Mutations)


class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        if self.path =="/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            print(data)
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404,{"Error":"Ruta no existente"})
            
def run_server(port = 8000):
    try:
        server_address = ("",port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()