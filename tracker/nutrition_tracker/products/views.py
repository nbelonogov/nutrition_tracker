from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from products.models import User, Product, ProductCategory, Meal
from products.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from products.serializers import UserSerializer, ProductSerializer, ProductCategorySerializer, MealSerializer


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )


class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )


class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)


class ProductCategoryList(ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class ProductCategoryDetail(RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = (IsAdminUser,)


class MealList(ListCreateAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MealDetail(RetrieveUpdateDestroyAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = (IsOwnerOrReadOnly,)


@login_required
def meal_add(request, product_id):
    product = Product.objects.get(id=product_id)
    dishes = Meal.objects.filter(user=request.user, product=product)

    if not dishes.exists():
        Meal.objects.create(user=request.user, product=product, weight=100)
    else:
        dish = dishes.first()
        dish.weight += 100
        dish.save()


@login_required
def meal_remove(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    meal.delete()