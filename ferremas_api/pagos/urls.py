from django.urls import path
from .views import WebpayInitView, WebpayResponse , redigir_webpay

urlpatterns = [
    path('webpay/init/', WebpayInitView.as_view(), name='webpay-init'),
    path('webpay/response/', WebpayResponse.as_view(), name='webpay-response'),
    path('redirigir_webpay/', redigir_webpay , name='redigir_webpay')
]