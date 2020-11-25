from django.conf import settings

MY_SETTING = getattr(settings, 'INCREASE_BY', '500')
