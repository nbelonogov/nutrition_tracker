from django.urls import path, include

from rest_framework import routers

from products.views import ProductViewSet, ProductCategoryViewSet, UserViewSet, MealViewSet

app_name = 'products'

router = routers.DefaultRouter()
router.register(r'meals', MealViewSet)
router.register(r'users', UserViewSet, basename='users')
router.register(r'products', ProductViewSet)
router.register(r'product-categories', ProductCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
