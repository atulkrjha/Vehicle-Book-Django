from django.contrib import admin
from .models import User, Bike, Station, Order
# Register your models here.

admin.site.register(User)
admin.site.register(Bike)
admin.site.register(Order)
admin.site.register(Station)

