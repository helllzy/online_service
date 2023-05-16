from django.contrib import admin
from knox import views as knox_views
import sys
sys.path.append("..shopping.views")
from shopping.views import RegisterAPI, LoginAPI
from django.urls import path, include

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('admin/', admin.site.urls),
    path('', include('shopping.urls'))
]