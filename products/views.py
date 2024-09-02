from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from products.models import Meal, Product, ProductCategory, User
from products.permissions import IsAdminOrReadOnly, IsOwner
from products.serializers import (MealSerializer, ProductCategorySerializer,
                                  ProductSerializer, UserSerializer)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return (permission() for permission in permission_classes)


class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class MealListView(generics.ListAPIView):
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Meal.objects.all()
        else:
            return Meal.objects.filter(user=self.request.user)


class MealCreateView(generics.CreateAPIView):
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MealDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MealSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user)
