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
    category = serializers.SlugRelatedField(label='Категория', slug_field='name',
                                            queryset=ProductCategory.objects.all())
    calories = serializers.ReadOnlyField()
    name = serializers.CharField(
        label='Название',
        validators=[RegexValidator(r'^[А-Яа-яЁё\s0-9]+$',
                                   message="Название продукта должно быть на русском языке.")])

    def validate_calories(self, value):
        # можно вынести также  вописание полей
        if value <= 0 or value > 10000:
            raise serializers.ValidationError("Значение калорий должно быть от 0 до 10000")
        return value

    # Падает с TypeError (пытаемся сравнить str < int и str > int)
    # def validate(self, attrs):
    #     for attr in attrs:
    #         if attr in ['proteins', 'fats', 'carbs']:
    #             if attr < 0 or attr > 99:
    #                 raise serializers.ValidationError("Введите допустимое значение")
    #     return attrs


class MealSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    total_calories = serializers.ReadOnlyField()

    class Meta:
        model = Meal
        fields = ('id', 'user', 'products', 'weight', 'total_calories')

    def create(self, validated_data):
        products = validated_data.pop('products')
        meal = Meal.objects.create(**validated_data)
        for product in products:
            product, _ = Product.objects.get_or_create(**product)
            meal.products.add(product)
        meal.calculate_total_calories()
        return meal
