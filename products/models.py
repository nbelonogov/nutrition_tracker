from django.contrib.auth.models import AbstractUser
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
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50, unique=True)
    proteins = models.IntegerField(verbose_name='Белки')
    fats = models.IntegerField(verbose_name='Жиры')
    carbs = models.IntegerField(verbose_name='Углеводы')
    category = models.ForeignKey(verbose_name='Категория', to=ProductCategory, on_delete=models.CASCADE)

    @property
    def calories(self):
        return (self.carbs + self.proteins)*4 + self.fats*9

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class MealQuerySet(models.QuerySet):
    def total_proteins(self):
        return sum(meal.sum_proteins() for meal in self)

    def total_fats(self):
        return sum(meal.sum_fats() for meal in self)

    def total_carbs(self):
        return sum(meal.sum_carbs() for meal in self)

    def total_calories(self):
        return sum(meal.sum_calories() for meal in self)


class Meal(models.Model):
    name = models.CharField(null=True, max_length=10, choices=[
        ('Завтрак', 'Завтрак'),
        ('Обед', 'Обед'),
        ('Ужин', 'Ужин')
    ])
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    products = models.ManyToManyField(to=Product, related_name='meals')
    weight = models.PositiveIntegerField(default=0)

    objects = MealQuerySet.as_manager()

    def __str__(self):
        return f'Прием пищи {self.user.username}'
