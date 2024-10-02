from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(AbstractUser):
    sex = models.CharField(verbose_name='Пол', max_length=10, null=True, choices=[
        ('М', 'Мужской'),
        ('Ж', 'Женский')
    ])
    weight = models.DecimalField(verbose_name='Вес', max_digits=3, decimal_places=1, null=True)
    height = models.IntegerField(verbose_name='Рост', null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class ProductCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50, unique=True)
    MIN_VALUE = 0
    MAX_VALUE = 99

    nutrients_validator = [
        MinValueValidator(MIN_VALUE),
        MaxValueValidator(MAX_VALUE)
    ]
    proteins = models.IntegerField(verbose_name='Белки', validators=nutrients_validator)
    fats = models.IntegerField(verbose_name='Жиры', validators=nutrients_validator)
    carbs = models.IntegerField(verbose_name='Углеводы', validators=nutrients_validator)
    category = models.ForeignKey(verbose_name='Категория', to=ProductCategory, on_delete=models.CASCADE)

    def calculate_calories(self):
        return (self.carbs + self.proteins)*4 + self.fats*9

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(null=True, max_length=10, choices=[
        ('Завтрак', 'Завтрак'),
        ('Обед', 'Обед'),
        ('Ужин', 'Ужин')
    ])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meals')
    products = models.ManyToManyField(Product, through='MealProduct')

    def total_proteins(self):
        return sum([meal_product.total_proteins() for meal_product in self.meal_products.all()])

    def total_fats(self):
        return sum([meal_product.total_fats() for meal_product in self.meal_products.all()])

    def total_carbs(self):
        return sum([meal_product.total_carbs() for meal_product in self.meal_products.all()])

    def total_calories(self):
        return sum([meal_product.total_calories() for meal_product in self.meal_products.all()])

    def __str__(self):
        return f'Прием пищи {self.user.username}'


class MealProduct(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='meal_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.FloatField()

    def total_proteins(self):
        return (self.product.proteins * self.weight) / 100

    def total_fats(self):
        return (self.product.fats * self.weight) / 100

    def total_carbs(self):
        return (self.product.carbs * self.weight) / 100

    def total_calories(self):
        return (self.product.calculate_calories() * self.weight) / 100
