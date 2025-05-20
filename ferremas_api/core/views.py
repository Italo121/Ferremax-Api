from rest_framework import viewsets
import asyncio
import random

import time
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse 
from .models import Sucursal, Producto, StockSucursal, Pedido, DetallePedido
from .serializers import SucursalSerializer, ProductoSerializer, StockSucursalSerializer, PedidoSerializer, DetallePedidoSerializer
import requests

class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class StockSucursalViewSet(viewsets.ModelViewSet):
    queryset = StockSucursal.objects.all()
    serializer_class = StockSucursalSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer
    
def event_stream():
    while True:
        sucursal = check_stock_levels()
        if sucursal:
            yield f"data: Stock bajo en {sucursal}\n\n"
        else:
            yield f"data: No falta stock en ninguna sucursal\n\n"
        time.sleep(15) 

def check_stock_levels():
    from .models import StockSucursal
    sucursal_con_stock_0 = StockSucursal.objects.filter(cantidad=0).first()
    if sucursal_con_stock_0:
        return sucursal_con_stock_0.sucursal.nombre  # Ajusta según tu modelo
    return None

def sse_stock_view(request):
    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response

def index(request):
    return HttpResponse("Bienvenido a Ferremas API")

def obtener_valor_dolar():
    try:
        api_key = "8ce3ef513b90b3f280dc4eec"
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
        response = requests.get(url)
        data = response.json()
        return data['conversion_rates']['CLP']
    except Exception as e:
        print("Error al obtener tipo de cambio:", e)
        return None

def precio_en_usd(request):
    tasa = obtener_valor_dolar()
    if tasa is None:
        return JsonResponse({'error': 'No se pudo obtener el tipo de cambio'}, status=500)

    stocks = StockSucursal.objects.all()
    Pedidos = DetallePedido.objects.all()

    data = []
    for stock in stocks:
        data.append({
            'producto': stock.producto,
            'sucursal': stock.sucursal,
            'cantidad': stock.cantidad,
            'precio': stock.precio,
            'precioUSD': round(stock.precio * tasa, 2)
        })
    for pedido in Pedidos:
        data.append({
            'pedido': pedido.pedido,
            'producto': pedido.producto,
            'cantidad': pedido.cantidad,
            'precio': pedido.precio_unitario,
            'precioUSD': round(pedido.precio_unitario * tasa, 2)
        })

    return JsonResponse({'productos': data})
