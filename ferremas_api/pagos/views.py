from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from transbank.webpay.webpay_plus.transaction import Transaction 
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType
from rest_framework import status
from django.http import JsonResponse
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys

class WebpayInitView(APIView):
    def post(self, request):
        options = WebpayOptions(
            commerce_code=IntegrationCommerceCodes.WEBPAY_PLUS,
            api_key=IntegrationApiKeys.WEBPAY,
            integration_type=IntegrationType.TEST
        )
        transaction = Transaction(options)

        buy_order = request.data.get("buy_order")
        session_id = request.data.get("session_id")
        amount = request.data.get("amount")
        return_url = "http://localhost:8000/api/pagos/webpay/response/"

        try:
            response = transaction.create(buy_order, session_id, amount, return_url)
            url = response['url']
            token = response['token']

            return render(request, 'redirigir_webpay.html', {
                "url": response ['url'],
                "token": response ['token']
            }, 
            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def webpay_response(request):
    if request.method == 'POST':
        token = request.POST.get('token_ws')
    elif request.method == 'GET':
        token = request.GET.get('token_ws')
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    if not token:
        return JsonResponse({'error': 'Token no entregado'}, status=400)

    options = WebpayOptions(
        commerce_code=IntegrationCommerceCodes.WEBPAY_PLUS,
        api_key=IntegrationApiKeys.WEBPAY,
        integration_type=IntegrationType.TEST
    )

    tx = Transaction(options)
    result = tx.commit(token)
    return JsonResponse(result)
    
def redirigir_webpay(request):
    return render(request, 'redirigir_webpay.html')

    

def iniciar_pago(request):
    return render(request, 'iniciar_pago.html')