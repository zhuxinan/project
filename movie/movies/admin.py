from django.contrib import admin

# Register your models here.
from .models import MyUser,Collections,Movies

admin.site.register(MyUser)
admin.site.register(Collections)
admin.site.register(Movies)