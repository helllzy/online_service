from django.urls import re_path, path
from .views import ListView, ProductView, BasketView, CreateDeleteUpdate

urlpatterns = [ 
    path("product/<int:id>", ProductView.view, name='product_view'),
    path("product/order", ProductView.order, name='order_product'),
    path("basket/add", BasketView.add, name='put_to_basket'),
    path("basket/view", BasketView.view, name='basket_view'),
    path("basket/clear", BasketView.clear, name='clear_product_in_basket'),
    path("basket/delete", BasketView.delete, name='delete_basket'),
    path("product/delete", CreateDeleteUpdate.delete, name='delete_product'),
    path("product/create", CreateDeleteUpdate.create, name='create_product'),
    path("product/update", CreateDeleteUpdate.update, name='update_product'),
    re_path(r"^(?P<api_name>[a-z]+)", ListView, name='online_service'),
]