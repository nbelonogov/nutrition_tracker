from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    sex = models.CharField(verbose_name='Пол', max_length=10, null=True, choices=[
        ('М', 'Мужской'),
        ('Ж', 'Женский')
    ])
    weight = models.DecimalField(verbose_name='Вес', max_digits=3, decimal_places=1, null=True)
    height = models.IntegerField(verbose_name='Рост', null=True)


class ProductCategory(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50)
    proteins = models.IntegerField(verbose_name='Белки')
    fats = models.IntegerField(verbose_name='Жиры')
    carbs = models.IntegerField(verbose_name='Углеводы')
    calories = models.IntegerField(verbose_name='Калории')
    category = models.ForeignKey(verbose_name='Категория', to=ProductCategory, on_delete=models.CASCADE)

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
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    weight = models.IntegerField(default=100)

    class Meta:
        verbose_name = 'Прием пищи'
        verbose_name_plural = 'Приемы пищи'

    def sum_calories(self):
        return self.product.calories * self.weight/100

    def total_calories_sum(self):
        food = Meal.objects.filter(user=self.user)
        return sum(dish.sum_calories() for dish in food)