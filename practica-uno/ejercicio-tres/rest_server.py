from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

pacientes = [
    {
        "ci":111111,
        "nombre":"Juan",
        "apellido":"Calamaro",
        "edad":21,
        "genero":"masculino",
        "diagnostico":"resfriado",
        "doctor":"mauricio_peredo",
    },
]

class PacientesService:    
    @staticmethod
    def crear_paciente(data):
        pacientes.append(data)
        return pacientes
    
    @staticmethod
    def buscar_paciente_ci(num_ci):
        for paciente in pacientes:
            if paciente["ci"]==int(num_ci):
                return paciente
        return None
    
    @staticmethod
    def listar_pacientes_diag(diagnostico):
        pacientes_diag=[]
        for paciente in pacientes:
            if paciente[diagnostico]==diagnostico:
                pacientes_diag.append(paciente)
        return pacientes_diag
    
    @staticmethod
    def buscar_pacientes_doctor(doctor):
        pacientes_doctor=[]
        for paciente in pacientes:
            if paciente["doctor"] == doctor:
                pacientes_doctor.append(paciente)
        return pacientes_doctor
    
    @staticmethod
    def actualizar_paciente(ci, data):
        paciente = PacientesService.buscar_paciente_ci(ci)
        if paciente:
            paciente.update(data)
            return pacientes
        else:
            return None
        
    @staticmethod
    def eliminar_paciente(ci):
        for i, paciente in enumerate(pacientes):
            if paciente["ci"]==ci:
                pacientes.pop(i)
                return paciente
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
        
        if parsed_path.path=="/pacientes":
            if "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientes_filtrados = PacientesService.buscar_pacientes_doctor(doctor)
                if pacientes_filtrados !=[]:
                    HTTPResponseHandler.handler_response(self,200,pacientes_filtrados)
                else:
                    HTTPResponseHandler.handler_response(self, 204, [])
            else:
                HTTPResponseHandler.handler_response(self,200,pacientes)
            
        elif self.path.startswith("/pacientes/"):
            id = int(self.path.split("/")[-1])
            paciente = PacientesService.buscar_paciente_ci(id)
            if paciente:
                HTTPResponseHandler.handler_response(self,200,[paciente])
            else:
                HTTPResponseHandler.handler_response(self, 204, [])
        else:
            HTTPResponseHandler.handler_response(self, 404, {"Error":"ruta no encontrada"})
    def do_POST(self):
        if self.path =="/pacientes":
            data = self.read_data()
            pacientes = PacientesService.crear_paciente(data)
            HTTPResponseHandler.handler_response(self, 201, pacientes)
        
        else:
            HTTPResponseHandler.handler_response(self,404,{"Error":"Ruta no existente"})
            
    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = int (self.path.split("/")[-1])
            data =self.read_data()
            paciente = PacientesService.actualizar_paciente(ci,data)
            if paciente:
                HTTPResponseHandler.handler_response(self,200,pacientes)
            else:
                HTTPResponseHandler.handler_response(self,400,{"error":"ruta no existente"})
        else:
            HTTPResponseHandler.handler_response(self,404, {"error":"ruta no existe"})
            
    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci =  int (self.path.split("/")[-1])
            pacientes = PacientesService.eliminar_paciente(ci)
            HTTPResponseHandler.handler_response(self,200,pacientes)
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