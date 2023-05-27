from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import Product
import sys
sys.path.append("..user")
from user.models import HistoryRow, History, User, Comment
from user.serializers import HistoryRowSerializer
from .serializers import ProductSerializer, CommentSerializer
from collections import namedtuple
import shutil
from config import PATH


nt = namedtuple("object", ["model", "serializers"])
pattern = {
    "product": nt(Product, ProductSerializer),
    "comment": nt(Comment, CommentSerializer),
    "historyrow": nt(HistoryRow, HistoryRowSerializer)
}


class CreateDeleteUpdate:
    @login_required
    @api_view(["POST"])
    def create(request):
        username = request.user.username
        user = User.objects.get(username=username)
        data = request.data
        name = data["name"]
        available_count = data["available_count"]
        price = data["price"]
        product = Product.objects.create(
            name=name,
            available_count=available_count,
            price=price
            )
        user.created_prods.add(product)
        if data.get("photo"):
            photo = data["photo"]
            product.photo = photo
            product.save()
            try:
                shutil.rmtree(PATH)
            except:
                print(f'the directory {PATH} wasn`t deleted')
        object = pattern.get('product')
        serializer = object.serializers(product)
        return Response(serializer.data)


    @login_required
    @api_view(["PUT"])
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
                return Response({'error': f'{user.id} isn`t the owner of the product'})
        else:
            return Response({'error': f'{user.id} didn`t put product id'})


    @login_required
    @api_view(["DELETE"])
    def delete(request):
        username = request.user.username
        user = User.objects.get(username=username)
        data = request.data
        if data.get("id"):
            id = data.get("id")
            if user.created_prods.get(id=id):
                product = Product.objects.get(id=id)
                product.delete()
                return Response({'message': f'{user.id} deleted the product'})
            else:
                return Response({'error': f'{user.id} isn`t the owner of the product'})
        else:
            return Response({'error': f'{user.id} didn`t put product id'})


class ProductView:
    @api_view(["GET"])
    def List(request):
        object = pattern.get('product')
        object_list = object.model.objects.filter(hidden=False)
        serializers = object.serializers(object_list, many=True)
        return Response(serializers.data)


    @api_view(["GET"])
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
            return Response({'error': f'{product.id} doesn`t available'})
        available = product.available_count
        if available >= count:
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
            if available - count == 0:
                product.hidden = True
            product.save()
            object = pattern.get('historyrow')
            serializer = object.serializers(history_row)
            return Response(serializer.data)
        else:
            product.hidden = True
            product.save()
            return Response({'message': f'{available} < {count}',
                             'error': f'{product.id} doesn`t have enough units'})