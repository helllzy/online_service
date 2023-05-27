from django.urls import path
from .views import BasketView

urlpatterns = [
    path("add", BasketView.add, name='put_to_basket'),
    path("view", BasketView.view, name='basket_view'),
    path("clear", BasketView.clear, name='clear_product_in_basket'),
    path("delete", BasketView.delete, name='delete_basket')
]