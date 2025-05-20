from django.urls import path
from . import views
from views import sse_stock_view

urlpatterns = [
    path('', views.index, name='index'),
    path("sse/stock/", sse_stock_view, name="sse_stock"),
    path("precio-en-usd/", views.precio_en_usd, name="precio_en_usd"),
]