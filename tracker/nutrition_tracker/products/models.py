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
    #убрать вес, тк это указывается в приеме пищи
    weight = models.FloatField(default=100)

    @property
    def calories(self):
        return (self.carbs + self.proteins)*4 + self.fats*9

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


#
class Meal(models.Model):
    name = models.CharField(null=True, max_length=10, choices=[
        ('Завтрак', 'Завтрак'),
        ('Обед', 'Обед'),
        ('Ужин', 'Ужин')
    ])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meals')
    products = models.ManyToManyField(Product, related_name='meals')
    weight = models.PositiveIntegerField()
    total_calories = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} пользователя {self.user.username}"

    def calculate_total_calories(self):
        total_calories = 0
        for product in self.products.all():
            total_calories += (product.calories * self.weight)/100
        self.total_calories = total_calories
        self.save()


# class Meal(models.Model):
#     name = models.CharField(null=True, max_length=10, choices=[
#         ('Завтрак', 'Завтрак'),
#         ('Обед', 'Обед'),
#         ('Ужин', 'Ужин')
#     ])
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE)
#     product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
#     # По идее один прием пищи должен содержать несколько продуктов, Arrays[Product]
#     weight = models.IntegerField(default=100)
#
#     def __str__(self):
#         return f"{self.name} пользователя {self.user.username}"
#
#     class Meta:
#         verbose_name = 'Прием пищи'
#         verbose_name_plural = 'Приемы пищи'
#
#     def sum_calories(self):
#         return self.product.calories * self.weight/100
#
#     def total_calories_sum(self):
#         food = Meal.objects.filter(user=self.user)
#         return sum(dish.sum_calories() for dish in food)
