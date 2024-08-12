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
        validators=[RegexValidator(r'^[А-Яа-яЁё\s0-9]+$',
                                   message="Название категории должно быть на русском языке.")])


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'proteins', 'fats', 'carbs', 'calories', 'category')

    name = serializers.CharField(
        validators=[RegexValidator(r'^[А-Яа-яЁё\s0-9]+$',
                                   message="Название продукта должно быть на русском языке.")])

    def validate_proteins(self, value):
        if value < 0 or value > 99:
            raise serializers.ValidationError("Введите допустимое значение")
        return value

    def validate_fats(self, value):
        if value < 0 or value > 99:
            raise serializers.ValidationError("Введите допустимое значение")
        return value

    def validate_carbs(self, value):
        if value < 0 or value > 99:
            raise serializers.ValidationError("Введите допустимое значение")
        return value

    def validate_calories(self, value):
        if value <= 0 or value > 1000:
            raise serializers.ValidationError("Введите допустимое значение")
        return value


class MealSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    sum_calories = fields.IntegerField(read_only=True)

    class Meta:
        model = Meal
        fields = ('id', 'name', 'product', 'user', 'weight', 'sum_calories')