from rest_framework import  status, generics, permissions
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import Product, User, Basket, Comment
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from .serializers import ProductSerializer, UserSerializer, RegisterSerializer, BasketSerializer, CommentSerializer
from collections import namedtuple
import os, glob
from config import PATH

nt = namedtuple("object", ["model", "serializers"])
pattern = {
    "product": nt(Product, ProductSerializer),
    "user": nt(User, UserSerializer),
    "basket": nt(Basket, BasketSerializer),
    "comment": nt(Comment, CommentSerializer),
}


class CreateDeleteUpdate:
    @login_required
    @api_view(["POST"])
    def create(request):
        username = request.user.username
        user = User.objects.get(username=username)
        name = request.data["name"]
        available_count = request.data["available_count"]
        price = request.data["price"]
        product = Product.objects.create(
            name=name,
            available_count=available_count,
            price=price
            )
        try:
            photo = request.data["photo"]
            product.photo = photo
            product.save()
            files = glob.glob(f'{PATH}/*')
            print(files)
            for fff in files:
                os.remove(fff)
        except:
            print('ky')
            pass
        user.created_prods.add(product)
        object = pattern.get('product', None)
        serializer = object.serializers(Product.objects.filter(id=product.id), many=True)
        return Response(serializer.data)


    @login_required
    @api_view(["POST"])
    def update(request):
        pass


    @login_required
    @api_view(["POST"])
    def delete(request):
        pass


class ProductView:
    @login_required
    @api_view(["POST"])
    def view(request, id):
        object = pattern.get('product', None)
        serializer = object.serializers(Product.objects.filter(id=id), many=True)
        return Response(serializer.data)


    @login_required
    @api_view(["POST"])
    def order(request):
        count = request.data["product_count"]
        username = request.user.username
        id = request.data["product_id"]
        product = Product.objects.get(id=id)
        if product.hidden == True:
            return Response({'product': product.id,
                             'error': 'product doesn`t available'})
        products = Product.objects.filter(id=id)
        available = product.available_count
        if available >= count:
            available -= count
            user = User.objects.get(username=username)
            user.bought_prods.add(product)
            products.update(available_count = F("available_count") - count)
            object = pattern.get('user', user)
            serializer = object.serializers(user)
            if available == 0:
                products.update(hidden=True)
            return Response(serializer.data)
        else:
            products.update(hidden=True)
            return Response({'product': product.id,
                            'available_count': available,
                            'want_to_order': count,
                            'error': 'don`t have enough products'})


class BasketView:
    @login_required
    @api_view(["POST"])#добавить колво добавляемого продукта
    def add(request):
        count = request.data["product_count"]
        username = request.user.username
        id = request.data["product_id"]
        user = User.objects.get(username=username)
        product = Product.objects.get(id=id)
        if product.hidden == True:
            return Response({'product': product.id,
                             'error': 'product doesn`t available'})
        try:
            basket = Basket.objects.get(user=user)
            basket.products.add(product)
        except:
            basket = Basket(user=user)
            basket.save()
            basket.products.add(product)
        object = pattern.get('basket', None)
        serializer = object.serializers(basket)
        return Response(serializer.data)
    

    @login_required
    @api_view(["POST"])#добавить колво убираемого продукта
    def clear(request):
        count = request.data["product_count"]
        username = request.user.username
        id = request.data["product_id"]
        user = User.objects.get(username=username)
        product = Product.objects.get(id=id)
        try:
            basket = Basket.objects.get(user=user)
            basket.products.remove(product)
            object = pattern.get('basket', None)
            serializer = object.serializers(basket)
            return Response(serializer.data)
        except:
            return Response({'error': 'don`t have a basket'})
    

    @login_required
    @api_view(["POST"])
    def view(request):
        username = request.user.username
        user = User.objects.get(username=username)
        try:
            basket = Basket.objects.get(user=user)
            object = pattern.get('basket', None)
            serializer = object.serializers(basket)
            return Response(serializer.data)
        except:
            return Response({'error': 'don`t have a basket'})
        

    @login_required
    @api_view(["POST"])
    def delete(request):
        username = request.user.username
        user = User.objects.get(username=username)
        try:
            basket = Basket.objects.get(user=user)
            basket.products.clear()
            return Response({'basket': 'deleted'})
        except:
            return Response({'error': 'don`t have a basket'})


@api_view(["GET"])
def ListView(request, api_name):
    object = pattern.get(api_name, None)
    if object == None:
        return Response(
            data = "Invalid URL",
            status = status.HTTP_404_NOT_FOUND,
        )
    if request.method == "GET":
        if api_name == 'product':
            object_list = object.model.objects.filter(hidden=False)
            serializers = object.serializers(object_list, many=True)
            return Response(serializers.data)
        else:
            return Response({'error': 'login necessary'})
        

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)