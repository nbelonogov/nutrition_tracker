from django.urls import include, path
from rest_framework import routers

from products.views import (MealCreateView, MealDetailView, MealListView,
                            ProductCategoryViewSet, ProductViewSet,
                            UserViewSet)

app_name = 'products'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'users')
router.register(r'products', ProductViewSet, 'products')
router.register(r'product-categories', ProductCategoryViewSet)

urlpatterns = [
    path('meals/', MealListView.as_view(), name='meal-list'),
    path('meals/create/', MealCreateView.as_view(), name='meal-create'),
    path('meals/<int:pk>/', MealDetailView.as_view(), name='meal-detail'),
    path('', include(router.urls)),
]
