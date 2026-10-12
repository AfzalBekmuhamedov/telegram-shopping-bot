from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from orders.models import Order
from products.models import Product
from orders.serializer import OrderSerializer

@api_view(['POST'])
def create_order(request):
    user_id = request.data.get('user_id')
    products = request.data.get("products")

    total_price = 0
    for p_id in products:
        product = Product.objects.get(id = p_id)
        total_price += product.price

    order = Order.objects.create(user_id=user_id,total_price=total_price)
    return Response({"message":"Order created","total_price":total_price})

    # serializer = OrderSerializer(data=request.data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data)
    # return Response(serializer.errors)

