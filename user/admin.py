from django.contrib import admin
from .models import User, History, HistoryRow

admin.site.register(User)
admin.site.register(History)
admin.site.register(HistoryRow)