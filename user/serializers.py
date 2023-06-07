from rest_framework import serializers
from .models import User, HistoryRow
from django.core.mail import send_mail
from knox.models import AuthToken
from online_service.settings import ALLOWED_HOSTS, EMAIL_HOST_USER


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ("id", "email", "is_active", "bought_prods", "created_prods", "username", "photo")


class HistoryRowSerializer(serializers.ModelSerializer):
    class Meta:
        model  = HistoryRow
        fields = ("product", "prod_count")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {'password': {'write_only': True}}
    
    def send_message(self, email, user, username):
        if ALLOWED_HOSTS:
            host = 'http://' + ALLOWED_HOSTS[0]
        else:
            host = 'http://localhost:8000'
        subject = "Helzy_developer"
        body_text = f"You must activate account on {host}/{username}/activate/{AuthToken.objects.create(user)[1]}"
        send_mail(subject, body_text, EMAIL_HOST_USER, [email, ], fail_silently=False)

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create_user(username, email, password)
        user.is_active = False
        user.save()
        self.send_message(email, user, username)
        return user
    

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)