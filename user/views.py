from rest_framework import generics, permissions
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from .models import User, HistoryRow, History
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from .serializers import UserSerializer, RegisterSerializer, HistoryRowSerializer, ChangePasswordSerializer
from collections import namedtuple
import shutil
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

PATH = f'{os.getcwd()}/media'
nt = namedtuple("object", ["model", "serializers"])
pattern = {
    "user": nt(User, UserSerializer),
    "historyrow": nt(HistoryRow, HistoryRowSerializer)
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
    @api_view(["PUT"])
    def user_edit(request, username):
        user = User.objects.get(username=username)
        data = request.data
        if data.get("new_photo"):
            new_photo = data["new_photo"]
            user.photo = new_photo
        if data.get("new_username"):
            new_username = data["new_username"]
            user.username = new_username
        user.save()
        try:
            shutil.rmtree(PATH)
        except:
            print(f'the directory {PATH} wasn`t deleted')
        object = pattern.get('user')
        serializer = object.serializers(user)
        return Response(serializer.data)
    
    class UserHistoryPaginated(generics.ListAPIView):
        @login_required
        @api_view(["GET"])
        def get(request, username):
            user = User.objects.get(username=username)
            try:
                history = History.objects.get(user=user)
            except:
                return Response({
                                'error': f'{user.id} doesn`t have a history'
                                })
            historyrow = HistoryRow.objects.filter(history=history)
            paginator = Paginator(historyrow, 3)
            page = request.data.get('page')
            try:
                 historyrow = paginator.page(page)
            except PageNotAnInteger:
                 historyrow = paginator.page(1)
            except EmptyPage:
                 historyrow = paginator.page(paginator.num_pages)
            object = pattern.get('historyrow')
            serializer = object.serializers(historyrow, many=True)
            return Response(serializer.data)


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
                        "user": serializer.data,
                        "message": "user must activate his account"
                        })
    @api_view(["GET", "POST"])
    def activate(self, username, token):
        user = User.objects.get(username=username)
        db_token = AuthToken.objects.get(user=user).token_key
        if db_token == token[:8]:
            user.is_active = True
            user.save()
            object = pattern.get('user')
            serializer = object.serializers(user)
            return Response({
                            "user": serializer.data
                            })
        else:
            return Response({
                            "message": "wrong token"
                            })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
    

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({
                                "message": "wrong password"
                                })
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({
                            'message': 'password updated successfully'
                            })

        return Response(serializer.errors)