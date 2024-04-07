from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class Paciente:
    def __init__(self):
        self.ci= None
        self.nombre= None
        self.apellido= None
        self.edad= None
        self.genero= None
        self.diagnostico= None
        self.doctor= None
    def __str__(self):
        return f"Ci:{self.ci}, Nombre:{self.nombre}, Apellido:{self.apellido}, Edad:{self.edad}, Genero:{self.genero}, Diagnostico:{self.diagnostico}, Doctor:{self.doctor}"

class PacienteBuilder:
    def __init__(self):
        self.paciente=Paciente()
    def set_ci(self,ci):
        self.paciente.ci = ci
    def set_nombre(self, nombre):
        self.paciente.nombre =nombre
    def set_apellido(self, apellido):
        self.paciente.apellido = apellido
    def set_edad(self, edad):
        self.paciente.edad=edad
    def set_genero(self, genero):
        self.paciente.genero = genero
    def set_diagnostico(self, diagnostico):
        self.paciente.diagnostico = diagnostico
    def set_doctor(self, doctor):
        self.paciente.doctor = doctor
    def get_paciente(self):
        return self.paciente

class Hospital:
    def __init__(self, builder):
        self.builder = builder
    def create_paciente(self, ci, nombre, apellido, edad, genero, diagnostico, doctor ):
        self.builder.set_ci(ci)
        self.builder.set_nombre(nombre)
        self.builder.set_apellido(apellido)
        self.builder.set_edad(edad)
        self.builder.set_genero(genero)
        self.builder.set_diagnostico(diagnostico)
        self.builder.set_doctor(doctor)
        return self.builder.get_paciente()

class PacientesService: 
    def __init__(self):
        self.builder = PacienteBuilder()
        self.directorPaciente = Hospital(self.builder)
    
    def handler_post_request(self, post_data):
        ci=post_data.get("ci",None)
        nombre=post_data.get("nombre",None)
        apellido=post_data.get("apellido",None)
        edad=post_data.get("edad",None)
        genero=post_data.get("genero",None)
        diagnostico=post_data.get("diagnostico",None)
        doctor=post_data.get("doctor",None)
        
        paciente = self.directorPaciente.create_paciente(ci, nombre, apellido, edad, genero, diagnostico, doctor)
        
        return{
            "ci":paciente.ci,
            "nombre":paciente.nombre,
            "apellido":paciente.apellido,
            "edad":paciente.edad,
            "genero":paciente.genero,
            "diagnostico":paciente.diagnostico,
            "doctor":paciente.doctor,
        }
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



class HTTPDataHandler:
    @staticmethod
    def handler_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type","applicatacion/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    @staticmethod
    def handler_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_Data = handler.rfile.read(content_length)
        return json.loads(post_Data.decode("utf-8"))
    
class PacienteHandler(BaseHTTPRequestHandler):
    def __init__(self, *args,**kwargs):
        controller = PacientesService()
        super().__init__(*args,**kwargs)
    def do_GET(self):
        parsed_path =urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if parsed_path.path=="/pacientes":
            if "doctor"in query_params:
                doctor = query_params["doctor"][0]
                pacientes_filtrados = PacientesService.buscar_pacientes_doctor(doctor)
                if pacientes_filtrados!=[]:
                    HTTPDataHandler.handler_response(self,200,pacientes_filtrados)
                else:
                    HTTPDataHandler.handler_response(self,204,[])
            else:
                HTTPDataHandler.handler_response(self, 200, pacientes)
        elif self.path.startswith("/pacientes/"):
            id = int(self.path.split("/")[-1])
            paciente = PacientesService.buscar_paciente_ci(id)
            if paciente:
                HTTPDataHandler.handler_response(self,200,[paciente])
            else:
                HTTPDataHandler.handler_response(self,404,{"error":"ruta no existente"})
        
    def do_POST(self):
        if self.path=="/pacientes":
            data = HTTPDataHandler.handler_reader(self)
            response_data = PacientesService().handler_post_request(data)
            pacientes.append(response_data)
            HTTPDataHandler.handler_response(self, 201, response_data)
        else:
            HTTPDataHandler.handler_response(self,404,{"error":"ruta no existente"})
    def do_PUT(self):
        if self.path.startswith("/pacientes"):
            ci =int (self.path.split("/")[-1])
            data = HTTPDataHandler.handler_reader(self)
            response_data = PacientesService.actualizar_paciente(ci, data)
            if response_data:
                HTTPDataHandler.handler_response(self,200,pacientes)
            else:
                HTTPDataHandler.handler_response(self,400,{"error":"ruta no existente"})
        else:
            HTTPDataHandler.handler_response(self,404, {"error":"ruta no existe"})
    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci =  int (self.path.split("/")[-1])
            pacientes = PacientesService.eliminar_paciente(ci)
            HTTPDataHandler.handler_response(self,200,pacientes)
        else:
            HTTPDataHandler.handler_response(self,404,{"error":"ruta no encontrada"})
def run(server_class=HTTPServer, handler_class=PacienteHandler,port=8000):
    server_address =("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()
if __name__ == "__main__":
    run()