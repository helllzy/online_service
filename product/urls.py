from django.urls import path
from .views import ProductView, CreateDeleteUpdate

urlpatterns = [
    path("<int:id>", ProductView.view, name='product_view'),
    path("order", ProductView.order, name='order_product'),
    path("comment", ProductView.add_comment, name='add_comment'),
    path("delete", CreateDeleteUpdate.delete, name='delete_product'),
    path("create", CreateDeleteUpdate.create, name='create_product'),
    path("update", CreateDeleteUpdate.update, name='update_product'),
]