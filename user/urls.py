from django.urls import path
from .views import UserFunctions, RegisterAPI, LoginAPI, ChangePasswordView
from knox import views as knox_views

urlpatterns = [
    path('register', RegisterAPI.as_view(), name='register'),
    path('login', LoginAPI.as_view(), name='login'),
    path('<str:username>/change_password', ChangePasswordView.as_view(), name='change_pass'),
    path('logout', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path("<str:username>", UserFunctions.user_info, name='user_info'),
    path("<str:username>/edit", UserFunctions.user_edit, name='user_edit'),
    path("<str:username>/activate/<str:token>", RegisterAPI.activate, name='user_activate'),
    path("<str:username>/view_history", UserFunctions.UserHistoryPaginated.get, name='user_view_history')
]