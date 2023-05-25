from django.contrib import admin
from .models import Product, User, Basket, Comment, History, HistoryRow, BasketRow

admin.site.register(Comment)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Basket)
admin.site.register(History)
admin.site.register(HistoryRow)
admin.site.register(BasketRow)