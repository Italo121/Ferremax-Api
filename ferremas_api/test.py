import grpc
from proto import service_pb2_grpc, service_pb2
from google.protobuf import empty_pb2

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = service_pb2_grpc.ProductoControllerStub(channel)

    # Crear producto
    nuevo = service_pb2.Producto(
        codigo="109",
        nombre="Producto Test",
        marca="MarcaX",
        descripcion="Desc de prueba"
    )
    creado = stub.Create(nuevo)
    print("Producto creado:", creado)

    # Recuperar producto usando codigo (string)
    try:
        producto = stub.Retrieve(service_pb2.ProductoRetrieveRequest(codigo=creado.codigo))
        print("Producto recuperado:", producto)
    except grpc.RpcError as e:
        print("Error al recuperar producto:", e.details())

    # Listar productos (stream)
    print("Lista de productos:")
    for prod in stub.List(service_pb2.ProductoListRequest()):
        print(prod)

    # Actualizar producto
    actualizado = service_pb2.Producto(
        codigo=creado.codigo,
        nombre="Nombre actualizado",
        marca=creado.marca,
        descripcion=creado.descripcion
    )
    actualizado_resp = stub.Update(actualizado)
    print("Producto actualizado:", actualizado_resp)

    # Borrar producto
    stub.Destroy(creado)
    print("Producto borrado")

if __name__ == "__main__":
    run()
