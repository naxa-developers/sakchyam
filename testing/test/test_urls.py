from django.urls import reverse, resolve
from django.test import TestCase
from dashboard.views import signup

#
#
# class TestUrls:
#
#     def test_core_partner_url(self):
#         path = reverse('partner')
#         assert resolve(path).view_name == "partner"
#
#     def test_core_program_url(self):
#         path = reverse('program')
#         assert resolve(path).view_name == "program"
#
#     def test_core_marker_category_url(self):
#         path = reverse('marker-category')
#         assert resolve(path).view_name == "marker-category"
#
#     def test_core_marker_value_url(self):
#         path = reverse('marker-value')
#         assert resolve(path).view_name == "marker-value"
#
#     def test_core_district_url(self):
#         path = reverse('district')
#         assert resolve(path).view_name == "district"
#
#     def test_core_province_url(self):
#         path = reverse('province')
#         assert resolve(path).view_name == "province"
#
#     def test_core_gapanapa_url(self):
#         path = reverse('gapanapa')
#         assert resolve(path).view_name == "gapanapa"
#
#     def test_core_fivew_url(self):
#         path = reverse('fivew')
#         assert resolve(path).view_name == "fivew"
#
#     def test_core_sector(self):
#         path = reverse('sector')
#         assert resolve(path).view_name == "sector"
#
#     def test_core_indicator_list(self):
#         path = reverse('indicator-list')
#         assert resolve(path).view_name == "indicator-list"
#
#     def test_core_indicator_value(self):
#         path = reverse('indicator-value')
#         assert resolve(path).view_name == "indicator-value"
#
#     def test_core_sub_sector(self):
#         path = reverse('sub-sector')
#         assert resolve(path).view_name == "sub-sector"
#
#     def test_dashboard_token(self):
#         path = reverse('token')
#         assert resolve(path).view_name == "token"


# class TestUrls(TestCase):
#
#     def test_signup_url_resolve_signup_view(self):
#         url = reverse('signup')
#         view = resolve(url)
#         self.assertEqual(view.func, signup)
#
#     def test_login_url_resolve_login_view(self):
#         url = reverse('login')
#         view = resolve(url)
#         self.assertEqual(view.view_name, 'login')
#
#     def test_logout_url_resolve_login_view(self):
#         url = reverse('logout')
#         view = resolve(url)
#         self.assertEqual(view.view_name, 'logout')
