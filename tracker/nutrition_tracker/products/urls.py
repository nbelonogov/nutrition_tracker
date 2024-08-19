from django.urls import path, include

from rest_framework import routers

from products.views import ProductViewSet, ProductCategoryViewSet, UserViewSet, MealViewSet

app_name = 'products'

router = routers.DefaultRouter()
router.register(r'meals', MealViewSet, 'meals')
router.register(r'users', UserViewSet, 'users')
router.register(r'products', ProductViewSet, 'products')
router.register(r'product-categories', ProductCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
