from decimal import Decimal
from math import isfinite

from external_currency.freecurrencyapi import convert
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from api import openapi
from api.serializers import CurrencySerializer


@openapi.currency
class CurrencyView(APIView):
    """
    Чтобы сконвертировать одну валюту в другую,
    используйте запрос с параметрами: from, to, amount.
    """

    def get(self, request, *args, **kwargs):
        serializer = CurrencySerializer(
            data=request.data,
            context={
                'request': request,
                'params': request.query_params,
                }
        )
        serializer.is_valid(raise_exception=True)

        from_param = serializer.validated_data['from']
        to_param = serializer.validated_data['to']
        amount_param = serializer.validated_data['amount']

        result = convert(
            from_param, to_param, amount_param
        )
        # DRF renders Decimal as float, which can overflow after conversion.
        if not isfinite(float(result)):
            raise ValidationError(
                'Результат выходит за допустимый диапазон. Уменьшите сумму.'
            )
        return Response(
            {
                'info': {
                    'rate': result/Decimal(amount_param),
                },
                'query': request.query_params,
                'result': result
            }
        )
