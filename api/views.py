from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from payments.payment import update_payment


@api_view(['POST', ])
def post_payment(request):
    """Обновляет платеж."""
    payment_id = request.data.get('object').get('id')
    if payment_id:
        update_payment(payment_id)
    return Response(status=status.HTTP_200_OK)
