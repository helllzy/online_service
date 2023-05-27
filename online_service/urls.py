from django.contrib import admin
from django.urls import path, include
import sys
sys.path.append("..product")
from product.views import ProductView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products', ProductView.List, name='products'),
    path('product/', include('product.urls')),
    path('basket/', include('basket.urls')),
    path('', include('user.urls'))
]