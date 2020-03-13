from django.test import RequestFactory
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase
from django.test import TestCase
from django.contrib.auth.models import User


# class TestViews(APITestCase, APIRequestFactory):
#
#     def test_partnernapi(self):
#         url = reverse('partner')
#         response = self.client.get(url, format='json')
#         assert response.status_code == 200
#
#     def test_programapi(self):
#         url = reverse('program')
#         response = self.client.get(url, format='json')
#         assert response.status_code == 200
#
#     def test_marker_category(self):
#         url = reverse('marker-category')
#         response = self.client.get(url, format='json')
#         assert response.status_code == 200
#
#     def test_marker_value(self):
#         url = reverse('marker-value')
#         response = self.client.get(url, format='json')
#         assert response.status_code == 200
#
#     def test_districtapi(self):
#         url = reverse('district')
#         response = self.client.get(url, format='json')
#         assert response.status_code == 200
#
#     def test_provinceapi(self):
#         url = reverse('province')
#         response = self.client.get(url, format='json')
#         assert response.status_code == 200
#
#     def test_gapanapaapi(self):
#         url = reverse('gapanapa')
#         response = self.client.get(url, format='json')
#         assert response.status_code == 200
#
#     def test_fivew(self):
#         url = reverse('fivew')
#         response = self.client.get(url, format='json')
#         assert response.status_code == 200
#
#     def test_sector(self):
#         url = reverse('sector')
#         response = self.client.get(url, format='json')
#         assert response.status_code == 200
#
#
#
#     def test_indicator_value(self):
#         url = reverse('indicator-value')
#         response = self.client.get(url, format='json')
#         assert response.status_code == 200
#
#     def test_sub_sector(self):
#         url = reverse('sub-sector')
#         response = self.client.get(url, format='json')
#         assert response.status_code == 200


class UserTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'sakchyam',
            'password': 'sakchyam@123'}
        User.objects.create_user(username='sakchyam', password='sakchyam@123')

    def test_signup_view_status_code(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_view_status_code(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # def test_logout_view_status_code(self):
    #     url = reverse('logout')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)

    # def test_user_login(self):
    #     response = self.client.post('/login', self.credentials)
    #     self.assertEqual(response.status_code, 200)



