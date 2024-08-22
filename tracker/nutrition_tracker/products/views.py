from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from products.models import User, Product, ProductCategory, Meal
from products.permissions import IsAdminOrReadOnly, IsOwner
from products.serializers import UserSerializer, ProductSerializer, ProductCategorySerializer, MealSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAdminUser, )
        return (permission() for permission in permission_classes)


class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class MealViewSet(ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Meal.objects.all()
        else:
            return Meal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            permission_classes = (IsAuthenticated, IsOwner)
        else:
            permission_classes = (IsAdminOrReadOnly, IsOwner)
        return (permission() for permission in permission_classes)
