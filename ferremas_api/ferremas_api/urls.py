from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import SucursalViewSet, ProductoViewSet, StockSucursalViewSet, PedidoViewSet, DetallePedidoViewSet, sse_stock_view, index, precio_en_usd


router = DefaultRouter()
router.register(r'sucursales', SucursalViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'stock', StockSucursalViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'detalles-pedido', DetallePedidoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('sse/stock/', sse_stock_view),
    path('', index),
    path('api/pagos/', include('pagos.urls')),
    path("api/precio-en-usd/", precio_en_usd, name="precio_en_usd"),
]