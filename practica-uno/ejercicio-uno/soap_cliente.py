from zeep import Client

cliente = Client("http://localhost:8000")
result01 = cliente.service.Sumar(num1=3,num2=4)
print(result01)

result02 = cliente.service.Resta(num1=6,num2=7)
print(result02)

result03 = cliente.service.Multiplicacion(num1=4,num2=5)
print(result03)

result04=cliente.service.Division(num1=4, num2=4)
print(result04)