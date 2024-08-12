from django.contrib import admin

from products.models import User, Product, ProductCategory

admin.site.register(User)
admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'proteins', 'fats', 'carbs', 'calories', 'category')
    fields = ('id', 'name', 'proteins', 'fats', 'carbs', 'calories', 'category')
    readonly_fields = ('id',)
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('category',)

