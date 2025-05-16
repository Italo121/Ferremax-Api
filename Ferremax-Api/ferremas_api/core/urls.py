from django.urls import path
from . import views
from views import sse_stock_view

urlpatterns = [
    path('', views.index, name='index'),
    path("sse/stock/", sse_stock_view, name="sse_stock"),
]