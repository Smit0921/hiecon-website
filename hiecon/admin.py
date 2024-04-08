from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Cartproduct)
admin.site.register(Solution)
admin.site.register(Newsletter)