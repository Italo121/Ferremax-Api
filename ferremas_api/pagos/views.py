from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from transbank.webpay.webpay_plus.transaction import Transaction 
from django.conf import settings

from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType
from rest_framework import status

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
            return Response({
                "url": response ['url'],
                "token": response ['token']
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class WebpayResponse(APIView):
    def post(self, request):
        token = request.data.get("token_ws")
        tx = Transaction()
        result = tx.commit(token)
        return Response(result)
