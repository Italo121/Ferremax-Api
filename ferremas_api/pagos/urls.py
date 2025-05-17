from django.urls import path
from .views import WebpayInitView, webpay_response , redirigir_webpay, iniciar_pago

urlpatterns = [
    path('webpay/init/', WebpayInitView.as_view(), name='webpay-init'),
    path('webpay/response/', webpay_response, name='webpay-response'),
    path('redirigir_webpay/', redirigir_webpay , name='redigir_webpay'),
    path('webpay/iniciar/', iniciar_pago, name='iniciar-pago'),

]