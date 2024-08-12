from django.contrib import admin

from products.models import User, Product, ProductCategory

admin.site.register(User)
admin.site.register(ProductCategory)
admin.site.register(Product)
