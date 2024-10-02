from django.contrib import admin

from products.models import Meal, Product, ProductCategory, User

admin.site.register(User)
admin.site.register(ProductCategory)
admin.site.register(Meal)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'proteins', 'fats', 'carbs', 'calories', 'category')
    fields = ('id', 'name', 'proteins', 'fats', 'carbs', 'category')
    readonly_fields = ('id', 'calories')
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('category',)