from django.core.validators import RegexValidator
from rest_framework import serializers

from products.models import Meal, Product, ProductCategory, User, MealProduct


class UserSerializer(serializers.ModelSerializer):
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



class MealProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = MealProduct
        fields = ['product', 'weight']


class MealSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    meal_products = MealProductSerializer(many=True, read_only=True)
    total_proteins = serializers.FloatField(read_only=True)
    total_fats = serializers.FloatField(read_only=True)
    total_carbs = serializers.FloatField(read_only=True)
    total_calories = serializers.FloatField(read_only=True)

    class Meta:
        model = Meal
        fields = ['id', 'name', 'user', 'products', 'weight', 'total_proteins',
                  'total_fats', 'total_carbs', 'total_calories']

    def get_total_proteins(self, obj):
        return sum(product.proteins for product in obj.products.all()) * obj.weight/100

    def get_total_fats(self, obj):
        return sum(product.fats for product in obj.products.all()) * obj.weight/100

    def get_total_carbs(self, obj):
        return sum(product.carbs for product in obj.products.all()) * obj.weight/100

    def get_total_calories(self, obj):
        return sum(product.calories for product in obj.products.all()) * obj.weight/100
