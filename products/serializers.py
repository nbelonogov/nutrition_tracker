from django.core.validators import RegexValidator
from rest_framework import serializers

from products.models import Meal, Product, ProductCategory, User


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


class MealSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    total_proteins = serializers.SerializerMethodField()
    total_fats = serializers.SerializerMethodField()
    total_carbs = serializers.SerializerMethodField()
    total_calories = serializers.SerializerMethodField()

    class Meta:
        model = Meal
        fields = ['id', 'name', 'user', 'products', 'weight', 'total_proteins',
                  'total_fats', 'total_carbs', 'total_calories']

    def create(self, validated_data):
        products = validated_data.pop('products')
        meal = Meal.objects.create(**validated_data)
        meal.products.set(products)
        meal.save()
        return meal

    def get_total_proteins(self, obj):
        return sum(product.proteins for product in obj.products.all()) * obj.weight/100

    def get_total_fats(self, obj):
        return sum(product.fats for product in obj.products.all()) * obj.weight/100

    def get_total_carbs(self, obj):
        return sum(product.carbs for product in obj.products.all()) * obj.weight/100

    def get_total_calories(self, obj):
        return sum(product.calories for product in obj.products.all()) * obj.weight/100


class AddProductsToMealSerializer(serializers.ModelSerializer):
    product_ids = serializers.ListField(child=serializers.IntegerField())

    def update(self, instance, validated_data):
        products = Product.objects.filter(id__in=validated_data['product_ids'])
        instance.products.add(*products)
        instance.save()
        return instance
