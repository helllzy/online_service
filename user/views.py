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
from config import PATH
from django.dispatch import Signal
from django.core.signing import BadSignature
from .utilities import send_activation_notification, signer

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
            try:
                shutil.rmtree(PATH)
            except:
                print(f'the directory {PATH} wasn`t deleted')
        if data.get("new_username"):
            new_username = data["new_username"]
            user.username = new_username
        user.save()
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
            return Response({'error': f'{user.id} doesn`t have a history'})
        historyrow = HistoryRow.objects.filter(history=history)
        object = pattern.get('historyrow')
        serializer = object.serializers(historyrow, many=True)
        return Response(serializer.data)
    

# class PaginatedUserViewHistory(generics.GenericAPIView):
#     def get(self, request, format=None):
#         product_sync_ts = request.GET.get(
#             'product_sync_ts', None)
#         if product_sync_ts:
#             product = GrProduct.objects.filter(
#                 update_ts__gt=product_sync_ts
#             )
#             paginator = Paginator(product, 1000)
#             page = request.GET.get('page')
#             try:
#                 product = paginator.page(page)
#             except PageNotAnInteger:
#                 product = paginator.page(1)
#             except EmptyPage:
#                 product = paginator.page(paginator.num_pages)

#             serializer = SyncedProductSerializer(
#                 instance={'products': product})
#             return paginator.get_paginated_response(serializer.data) # <- here it is
#         else:
#             content = {'details': "Bad Request"}
#             raise APIException400(request, content)

    


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
    


user_registered = Signal(providing_args=['instance'])

def user_registered_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])
    
user_registered.connect(user_registered_dispatcher)

def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return Response({'error': 'bad signature'})
    user = get_object_or_404(User, username=username)
    if user.is_activated:
        return Response({'message': 'user already activated'})
    else:
        user.is_active = True
        user.is_activated = True
        user.save()
    return Response({'message': 'activation_done'})




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
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]})
            # Set password
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'message': 'Password updated successfully'
            }

            return Response(response)

        return Response(serializer.errors)