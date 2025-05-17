from django.urls import path
from .views import WebpayInitView, WebpayResponse

urlpatterns = [
    path('webpay/init/', WebpayInitView.as_view(), name='webpay-init'),
    path('webpay/response/', WebpayResponse.as_view(), name='webpay-response'),
]