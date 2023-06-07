from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from .models import Product, Basket, BasketRow
import sys
sys.path.append("..user.models")
from user.models import User
from .serializers import BasketSerializer, BasketRowSerializer
from collections import namedtuple

nt = namedtuple("object", ["model", "serializers"])
pattern = {
    "basket": nt(Basket, BasketSerializer),
    "basketrow": nt(BasketRow, BasketRowSerializer),
}


class BasketView:
    @login_required
    @api_view(["POST"])
    def add(request):
        count = request.data["product_count"]
        username = request.user.username
        id = request.data["product_id"]
        user = User.objects.get(username=username)
        product = Product.objects.get(id=id)
        if product.hidden == True:
            return Response({
                            'error': f'{product.id} doesn`t available'
                            })
        try:
            basket = Basket.objects.get(user=user)
        except:
            basket = Basket.objects.create(user=user)
        try:
            basketrow = BasketRow.objects.get(basket = basket, product = product)
            basketrow.prod_count += count
            basketrow.save()
        except:
            basketrow = BasketRow.objects.create(
                basket = basket,
                product = product,
                prod_count = count
            )
        object = pattern.get('basketrow')
        serializer = object.serializers(basketrow)
        return Response(serializer.data)
    

    @login_required
    @api_view(["PUT"])
    def clear(request):
        count = request.data["product_count"]
        username = request.user.username
        id = request.data["product_id"]
        user = User.objects.get(username=username)
        product = Product.objects.get(id=id)
        try:
            basket = Basket.objects.get(user=user)
            basketrow = BasketRow.objects.get(basket=basket, product = product)
            if basketrow.prod_count <= count:
                basketrow.delete()
                return Response({
                                'message': f'{product.id} deleted from {basket.id}'
                                })
            else:
                basketrow.prod_count -= count
            basketrow.save()
            object = pattern.get('basketrow')
            serializer = object.serializers(basketrow)
            return Response(serializer.data)
        except:
            return Response({
                            'error': f'{user.id} doesn`t have a basket'
                            })
    

    @login_required
    @api_view(["GET"])
    def view(request):
        username = request.user.username
        user = User.objects.get(username=username)
        try:
            basket = Basket.objects.get(user=user)
        except:
            return Response({
                            'error': f'{user.id} doesn`t have a basket'
                            })
        basketrow = BasketRow.objects.filter(basket=basket)
        sum = 0
        for i in basketrow:
            sum+=i.product.price*i.prod_count
        basket_price = sum
        object = pattern.get('basketrow')
        serializer = object.serializers(basketrow, many=True)
        return Response({
                        "data": serializer.data,
                        "basket_price": basket_price
                        })
    

    @login_required
    @api_view(["DELETE"])
    def delete(request):
        username = request.user.username
        user = User.objects.get(username=username)
        try:
            basket = Basket.objects.get(user=user)
            basket.delete()
            return Response({
                            'message': f'{user.id} deleted the basket'
                            })
        except:
            return Response({
                            'error': f'{user.id} doesn`t have a basket'
                            })