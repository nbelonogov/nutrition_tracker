from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


from products.models import User


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='admin123'
        )
        self.regular_user = User.objects.create_user(
            username='regular', email='regular@example.com', password='regular123'
        )

    def test_list_users_as_admin(self):
        self.client.login(user=self.admin_user)
        url = reverse('users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_users_as_regular_user(self):
        self.client.login(user=self.regular_user)
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
