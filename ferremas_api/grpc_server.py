import os
import django
import grpc
from concurrent import futures

# Configura Django para poder usar sus modelos
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ferremas_api.settings")
django.setup()

from proto import service_pb2_grpc, service_pb2
from google.protobuf import empty_pb2

# Importa tu modelo Django (ajusta app y modelo)
from core.models import Producto as ProductoModel

class ProductoController(service_pb2_grpc.ProductoControllerServicer):

    def List(self, request, context):
        # Ejemplo: stream de todos los productos
        for prod in ProductoModel.objects.all():
            yield service_pb2.Producto(
                codigo=prod.codigo,
                nombre=prod.nombre,
                marca=prod.marca,
                descripcion=prod.descripcion
            )

    def Create(self, request, context):
        prod = ProductoModel.objects.create(
            codigo=request.codigo,
            nombre=request.nombre,
            marca=request.marca,
            descripcion=request.descripcion
        )
        return service_pb2.Producto(
            codigo=prod.codigo,
            nombre=prod.nombre,
            marca=prod.marca,
            descripcion=prod.descripcion
        )

    def Retrieve(self, request, context):
        try:
            prod = ProductoModel.objects.get(codigo=request.codigo)
            return service_pb2.Producto(
                codigo=prod.codigo,
                nombre=prod.nombre,
                marca=prod.marca,
                descripcion=prod.descripcion
            )
        except ProductoModel.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Producto no encontrado')
            return service_pb2.Producto()  # Devuelve vacío

    def Update(self, request, context):
        try:
            prod = ProductoModel.objects.get(codigo=request.codigo)
            prod.codigo = request.codigo
            prod.nombre = request.nombre
            prod.marca = request.marca
            prod.descripcion = request.descripcion
            prod.save()
            return service_pb2.Producto(
                codigo=prod.codigo,
                nombre=prod.nombre,
                marca=prod.marca,
                descripcion=prod.descripcion
            )
        except ProductoModel.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Producto no encontrado')
            return service_pb2.Producto()

    def Destroy(self, request, context):
        try:
            prod = ProductoModel.objects.get(codigo=request.codigo)
            prod.delete()
            return empty_pb2.Empty()
        except ProductoModel.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Producto no encontrado')
            return empty_pb2.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_ProductoControllerServicer_to_server(ProductoController(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC corriendo en puerto 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

