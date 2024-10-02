from django.contrib import admin

from products.models import Meal, Product, ProductCategory, User

admin.site.register(User)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Meal)
