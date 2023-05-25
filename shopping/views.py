from rest_framework import  status, generics, permissions
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import Product, User, Basket, BasketRow, Comment, HistoryRow, History
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from .serializers import ProductSerializer, UserSerializer, RegisterSerializer, BasketSerializer, CommentSerializer, HistoryRowSerializer, BasketRowSerializer
from collections import namedtuple
import shutil
from config import PATH

nt = namedtuple("object", ["model", "serializers"])
pattern = {
    "product": nt(Product, ProductSerializer),
    "user": nt(User, UserSerializer),
    "basket": nt(Basket, BasketSerializer),
    "comment": nt(Comment, CommentSerializer),
    "historyrow": nt(HistoryRow, HistoryRowSerializer),
    "basketrow": nt(BasketRow, BasketRowSerializer),
}

class UserFunctions:
    @login_required
    @api_view(["GET"])
    def user_info(request, username):
        user = User.objects.get(username=username)
        object = pattern.get('user')
        serializer = object.serializers(user)
        return Response(serializer.data)
    

    @login_required
    @api_view(["POST"])
    def user_edit_username(request, username):
        user = User.objects.get(username=username)
        new_username = request.data["new_username"]
        user.username = new_username
        user.save()
        object = pattern.get('user')
        serializer = object.serializers(user)
        return Response(serializer.data)


    @login_required
    @api_view(["POST"])
    def user_edit_photo(request, username):
        user = User.objects.get(username=username)
        new_photo = request.data["new_photo"]
        user.photo = new_photo
        user.save()
        try:
            shutil.rmtree(PATH)
        except:
            print(f'the directory {PATH} wasn`t deleted')
        object = pattern.get('user')
        serializer = object.serializers(user)
        return Response(serializer.data)
    

    @login_required
    @api_view(["GET"])
    def user_view_history(request, username):
        user = User.objects.get(username=username)
        try:
            history = History.objects.get(user=user)
        except:
            return Response({"You haven`t history yet"})
        historyrow = HistoryRow.objects.filter(history=history)
        object = pattern.get('historyrow')
        serializer = object.serializers(historyrow, many=True)
        return Response(serializer.data)


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
        if request.data.get("photo"):
            photo = request.data["photo"]
            product.photo = photo
            product.save()
            try:
                shutil.rmtree(PATH)
            except:
                print(f'the directory {PATH} wasn`t deleted')
        user.created_prods.add(product)
        object = pattern.get('product')
        serializer = object.serializers(product)
        return Response(serializer.data)


    @login_required
    @api_view(["POST"])
    def update(request):
        username = request.user.username
        user = User.objects.get(username=username)
        data = request.data
        if data.get("id"):
            id = data.get("id")
            product = Product.objects.get(id=id)
            if user.created_prods.get(id=id):
                if data.get("name"):
                    name = data.get("name")
                    product.name = name
                if data.get("available_count"):
                    available_count = data.get("available_count")
                    product.available_count = available_count
                if data.get("price"):
                    price = data.get("price")
                    product.price = price
                if data.get("photo"):
                    photo = data.get("photo")
                    product.photo = photo
                    try:
                        shutil.rmtree(PATH)
                    except:
                        print(f'the directory {PATH} didn`t deleted')
                product.save()
                object = pattern.get('product')
                serializer = object.serializers(product)
                return Response(serializer.data)
            else:
                return Response({'error': 'user isn`t the owner of the product'})
        else:
            return Response({'error': 'user didn`t give product id'})


    @login_required
    @api_view(["POST"])
    def delete(request):
        username = request.user.username
        user = User.objects.get(username=username)
        data = request.data
        if data.get("id"):
            id = data.get("id")
            if user.created_prods.get(id=id):
                product = Product.objects.get(id=id)
                product.delete()
                object = pattern.get('user')
                serializer = object.serializers(user)
                return Response(serializer.data)
            else:
                return Response({'error': 'user isn`t the owner of the product'})
        else:
            return Response({'error': 'user didn`t give product id'})


class ProductView:
    @api_view(["POST"])
    def view(request, id):
        product = Product.objects.get(id=id)
        object1 = pattern.get('product')
        object2 = pattern.get('comment')
        prod_serializer = object1.serializers(product)
        comms_serializer = object2.serializers(Comment.objects.filter(product=product), many=True)
        return Response({"product_data": prod_serializer.data, "comments_data": comms_serializer.data})
    

    @login_required
    @api_view(["POST"])
    def add_comment(request):
        username = request.user.username
        user = User.objects.get(username=username)
        product_id = request.data["product_id"]
        comment_text = request.data["comment"]
        product = Product.objects.get(id=product_id)
        rate = request.data["rate"]
        comment = Comment.objects.create(
            comment = comment_text,
            product = product,
            user = user,
            rate = rate
        )
        len_comm = len(Comment.objects.filter(product=product))
        product.rate = f'{((product.rate*(len_comm-1)+float(rate))/len_comm):.1f}'
        product.save()
        if request.data.get("photo"):
            photo = request.data["photo"]
            comment.photo = photo
            comment.save()
            try:
                shutil.rmtree(PATH)
            except:
                print(f'the directory {PATH} wasn`t deleted')
        object = pattern.get('comment')
        serializer = object.serializers(comment)
        return Response({'data': serializer.data, 'rate': product.rate})


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
        available = product.available_count
        if available >= count:
            available -= count
            user = User.objects.get(username=username)
            user.bought_prods.add(product)
            try:
                history = History.objects.get(user=user)
            except:
                history = History.objects.create(
                    user = user
                )
            history_row = HistoryRow.objects.create(
                history = history,
                product = product,
                prod_count = count
            )
            product.available_count = F("available_count") - count
            if available == 0:
                product.hidden = True
            object = pattern.get('historyrow')
            serializer = object.serializers(history_row)
            return Response(serializer.data)
        else:
            product.hidden = True
            return Response({'product': product.id,
                            'available_count': available,
                            'want_to_order': count,
                            'error': 'don`t have enough products'})


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
            return Response({'product': product.id,
                             'error': 'product doesn`t available'})
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
    @api_view(["POST"])
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
                return Response({'basketrow': 'deleted'})
            else:
                basketrow.prod_count -= count
            basketrow.save()
            object = pattern.get('basketrow')
            serializer = object.serializers(basketrow)
            return Response(serializer.data)
        except:
            return Response({'error': 'don`t have a basket yet'})
    

    @login_required
    @api_view(["POST"])
    def view(request):
        username = request.user.username
        user = User.objects.get(username=username)
        try:
            basket = Basket.objects.get(user=user)
        except:
            return Response({'error': 'don`t have a basket yet'})
        basketrow = BasketRow.objects.filter(basket=basket)
        sum = 0
        for i in basketrow:
            sum+=i.product.price*i.prod_count
        basket_price = sum
        object = pattern.get('basketrow')
        serializer = object.serializers(basketrow, many=True)
        return Response({"data": serializer.data, "basket_price": basket_price})
    

    @login_required
    @api_view(["POST"])
    def delete(request):
        username = request.user.username
        user = User.objects.get(username=username)
        try:
            basket = Basket.objects.get(user=user)
            basket.delete()
            return Response({'basket': 'deleted'})
        except:
            return Response({'error': 'don`t have a basket yet'})


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