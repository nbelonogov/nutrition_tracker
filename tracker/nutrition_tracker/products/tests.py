from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from products.models import User, ProductCategory, Product, Meal


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username='user1', email='user1@example.com')
        self.admin_user = User.objects.create_superuser(
            username='admin123', email='admin123@example.com', password='admin123'
        )
        self.regular_user = User.objects.create_user(
            username='regular', email='regular@example.com', password='regular123'
        )

    def test_list_users_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('products:users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_users_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('products:users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('products:users-detail', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user1.username)

    def test_retrieve_user_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('products:users-detail', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('products:users-list')
        data = {'username': 'newuser', 'email': 'newuser@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)

    def test_create_user_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('products:users-list')
        data = {'username': 'newuser', 'email': 'newuser@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 3)

    def test_update_user_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('products:users-detail', args=[self.user1.id])
        data = {'username': 'updateduser'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'updateduser')

    def test_update_user_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('products:users-detail', args=[self.user1.id])
        data = {'username': 'updateduser'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, self.user1.username)

    def test_delete_user_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('products:users-detail', args=[self.user1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 2)

    def test_delete_user_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('products:users-detail', args=[self.user1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 3)


class ProductCategoryViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin123', email='admin123@example.com', password='admin123'
        )
        self.category1 = ProductCategory.objects.create(name='Category 1')

    def test_list_productcategories(self):
        url = reverse('products:productcategory-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ProductCategory.objects.count(), 1)
        self.assertEqual(response.data[0]['name'], 'Category 1')

    def test_retrieve_productcategory(self):
        url = reverse('products:productcategory-detail', kwargs={'pk': self.category1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Category 1')

    def test_create_productcategory(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('products:productcategory-list')
        data = {'name': 'Категория 2'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Категория 2')

    def test_update_productcategory(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('products:productcategory-detail', kwargs={'pk': self.category1.id})
        data = {'name': 'Измененная категория'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Измененная категория')

    def test_delete_productcategory(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('products:productcategory-detail', kwargs={'pk': self.category1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ProductCategory.objects.count(), 0)


class ProductViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = ProductCategory.objects.create(name='Категория')
        self.product = Product.objects.create(name='Продукт 1', proteins=10, fats=5,
                                              carbs=20, category=self.category)
        self.admin_user = User.objects.create_superuser(
            username='admin123', email='admin123@example.com', password='admin123'
        )
        self.regular_user = User.objects.create_user(
            username='regular', email='regular@example.com', password='regular123'
        )

    def test_get_product_list_as_anonymous(self):
        url = reverse('products:products-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_products_as_authenticated(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('products:products-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)

    def test_get_product_detail_as_anonymous(self):
        url = reverse('products:products-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_product_detail_as_authenticated(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('products:products-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Продукт 1')

    def test_get_product_detail_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('products:products-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Продукт 1')

    def test_create_product_as_regular(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('products:products-list')
        data = {
            'name': 'Продукт 2',
            'proteins': 10,
            'fats': 5,
            'carbs': 20,
            'category': self.category.name
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.count(), 1)

    def test_create_product_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('products:products-list')
        data = {
            'name': 'Продукт 2',
            'proteins': 10,
            'fats': 5,
            'carbs': 25,
            'category': self.category.name
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_update_product_as_regular(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('products:products-detail', args=[self.product.id])
        data = {'name': 'Измененный продукт'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('products:products-detail', args=[self.product.id])
        data = {'name': 'Измененный продукт'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Измененный продукт')

    def test_delete_product_as_regular(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('products:products-detail', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.count(), 1)

    def test_delete_product_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('products:products-detail', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)


# class MealViewSetTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.admin_user = User.objects.create_superuser(
#             username='admin123', email='admin123@example.com', password='admin123'
#         )
#         self.user1 = User.objects.create_user(username='user1', password='password1')
#         self.category = ProductCategory.objects.create(name='Категория')
#         self.product1 = Product.objects.create(name='Продукт 1', proteins=10, fats=5,
#                                                carbs=20, category=self.category)
#         self.meal1 = Meal.objects.create(name='Meal 1', user=self.user1)
#         self.meal1.products.create(name='Продукт 1', proteins=10, fats=5,
#                                    carbs=20, category=self.category)
#         self.meal1.save()
#         self.meal1.total_calories += self.product1.calories()
#
#     def test_list_meals_as_admin(self):
#         self.client.force_authenticate(user=self.admin_user)
#         url = reverse('products:meals-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Meal.objects.count(), 1)
