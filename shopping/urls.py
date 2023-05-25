from django.urls import re_path, path
from .views import ListView, ProductView, BasketView, CreateDeleteUpdate, UserFunctions

urlpatterns = [
    path("user/<str:username>", UserFunctions.user_info, name='user_info'),
    path("user/<str:username>/edit_username", UserFunctions.user_edit_username, name='user_edit_username'),
    path("user/<str:username>/edit_photo", UserFunctions.user_edit_photo, name='user_edit_photo'),
    path("user/<str:username>/view_history", UserFunctions.user_view_history, name='user_view_history'),
    path("product/<int:id>", ProductView.view, name='product_view'),
    path("product/order", ProductView.order, name='order_product'),
    path("product/comment", ProductView.add_comment, name='add_comment'),
    path("basket/add", BasketView.add, name='put_to_basket'),
    path("basket/view", BasketView.view, name='basket_view'),
    path("basket/clear", BasketView.clear, name='clear_product_in_basket'),
    path("basket/delete", BasketView.delete, name='delete_basket'),
    path("product/delete", CreateDeleteUpdate.delete, name='delete_product'),
    path("product/create", CreateDeleteUpdate.create, name='create_product'),
    path("product/update", CreateDeleteUpdate.update, name='update_product'),
    re_path(r"^(?P<api_name>[a-z]+)", ListView, name='online_service'),
]