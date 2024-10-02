from django.urls import include, path
from rest_framework import routers

from products.views import (ProductCategoryViewSet, ProductViewSet, UserViewSet, MealViewSet)

app_name = 'products'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'users')
router.register(r'categories', ProductCategoryViewSet, 'categories')
router.register(r'products', ProductViewSet, 'products')
router.register(r'meals', UserViewSet, 'meals')


urlpatterns = [
    path('', include(router.urls)),
]
