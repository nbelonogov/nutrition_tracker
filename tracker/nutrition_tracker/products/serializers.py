from django.core.validators import RegexValidator
from rest_framework import serializers, fields

from products.models import User, ProductCategory, Product, Meal


class UserSerializer(serializers.ModelSerializer):
    meals = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'meals', 'is_staff')


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name')

    name = serializers.CharField(
        label='Название',
        validators=[RegexValidator(r'^[А-Яа-яЁё\s0-9]+$',
                                   message="Название категории должно быть на русском языке.")])


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'proteins', 'fats', 'carbs', 'calories', 'category')

    error_messages = {
        'min_value': 'Значение должно быть положительным.',
        'max_value': 'Значение не должно превышать 99.'
    }
    proteins = serializers.IntegerField(label='Белки', min_value=0, max_value=99, error_messages=error_messages)
    fats = serializers.IntegerField(label='Жиры', min_value=0, max_value=99, error_messages=error_messages)
    carbs = serializers.IntegerField(label='Углеводы', min_value=0, max_value=99, error_messages=error_messages)
    category = serializers.SlugRelatedField(label='Категория',
                                            slug_field='name',
                                            queryset=ProductCategory.objects.all())
    calories = serializers.IntegerField(label='Калории',
                                        read_only=True,
                                        min_value=0,
                                        max_value=10000,
                                        error_messages={
                                            'min_value': 'Значение должно быть положительным.',
                                            'max_value': 'Значение не должно превышать 10000.'
                                        })
    name = serializers.CharField(
        label='Название',
        validators=[RegexValidator(r'^[А-Яа-яЁё\s0-9]+$',
                                   message="Название продукта должно быть на русском языке.")])


# class MealSerializer(serializers.ModelSerializer):
#     products = ProductSerializer(many=True, read_only=True)
#     user = serializers.PrimaryKeyRelatedField(read_only=True)
#     total_calories = serializers.ReadOnlyField()
#
#     class Meta:
#         model = Meal
#         fields = ('id', 'name', 'user', 'products', 'weight', 'total_calories')

class MealSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    total_calories = serializers.SerializerMethodField()

    class Meta:
        model = Meal
        fields = ['id', 'name', 'user', 'products', 'weight', 'total_calories']

    def get_total_calories(self, obj):
        total_calories = 0
        for product in obj.products.all():
            total_calories += product.calories()
        return total_calories
