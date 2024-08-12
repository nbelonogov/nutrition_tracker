from django.urls import path

from products.views import UserList, UserDetail, ProductList, ProductDetail, ProductCategoryList, ProductCategoryDetail, MealList, MealDetail

app_name = 'products'

urlpatterns = [
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('products/', ProductList.as_view()),
    path('products/<int:pk>/', ProductDetail.as_view()),
    path('product-categories/', ProductCategoryList.as_view()),
    path('product-categories/<int:pk>/', ProductCategoryDetail.as_view()),
    path('meals/', MealList.as_view()),
    path('meals/<int:pk>/', MealDetail.as_view()),
]
