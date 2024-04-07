from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

animales=[
    {
        "id":1,
        "nombre":"garfield",
        "especie":"felino",
        "genero":"hembra",
        "edad":12,
        "peso":24
    }
]

class AnimalesService:
    @staticmethod
    def animal_por_id(id):
        for animal in animales:
            if animal["id"]==id:
                return animal
        return None
    def crear_animal(data):
        animales.append(data)
        return animales
    
    def animales_por_especie(especie):
        especie_animales=[]
        for animal in animales:
            if animal["especie"]==especie:
                especie_animales.append(animal)
        return especie_animales
    def animales_por_genero(genero):
        genero_animales=[]
        for animal in animales:
            if animal["genero"]==genero:
                genero_animales.append(animal)
        return genero_animales
    def actualizar_animal(id,data):
        animal=AnimalesService.animal_por_id(id)
        if animal:
            animal.update(data)
            return animales
        else:
            return None
    def eliminar_animal(id):
        for i, animal in enumerate(animales):
            if animal["id"]==id:
                animales.pop(i)
                return animal
        return None
    
class HTTPResponseHandler:
    @staticmethod
    def handler_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type","applicatacion/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
        
class RESTRequestHandler(BaseHTTPRequestHandler):
    def read_data(self):
        content_length=int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if parsed_path.path =="/animales":
            if "especie"in query_params:
                especie =query_params["especie"][0]
                animales_filtrados_especie = AnimalesService.animales_por_especie(especie)
                if animales_filtrados_especie !=[]:
                    print("hola")
                    HTTPResponseHandler.handler_response(self,200,animales_filtrados_especie)
                else:
                    HTTPResponseHandler.handler_response(self, 204,[])
            elif "genero" in query_params:
                genero = query_params["genero"][0]
                animales_filtrados_genero = AnimalesService.animales_por_genero(genero)
                if animales_filtrados_genero!=[]:
                    HTTPResponseHandler.handler_response(self,200,animales_filtrados_genero)
                else:
                    HTTPResponseHandler.handler_response(self,204,[])
            else:
                HTTPResponseHandler.handler_response(self,200,animales)
        else:
            HTTPResponseHandler.handler_response(self,404,{"error":"ruta no encontrada"})
    def do_POST(self):
        if self.path =="/animales":
            data = self.read_data()
            animales= AnimalesService.crear_animal(data)
            HTTPResponseHandler.handler_response(self,201, animales)
        else:
            HTTPResponseHandler.handler_response(self,404,{"error":"ruta no existente"})
    def do_PUT(self):
        if self.path.startswith("/animales/"):
            ci = int (self.path.split("/")[-1])
            data =self.read_data()
            animal = AnimalesService.actualizar_animal(ci,data)
            if animal:
                HTTPResponseHandler.handler_response(self,200,animales)
            else:
                HTTPResponseHandler.handler_response(self,400,{"error":"ruta no existente"})
        else:
            HTTPResponseHandler.handler_response(self,404, {"error":"ruta no existe"})
    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            ci =  int (self.path.split("/")[-1])
            animales = AnimalesService.eliminar_animal(ci)
            HTTPResponseHandler.handler_response(self,200,animales)
        else:
            HTTPResponseHandler.handler_response(self,404,{"error":"ruta no encontrada"})
def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()