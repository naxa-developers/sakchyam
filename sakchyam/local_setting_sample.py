DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'sakchyam_db',
        'USER': 'postgres',
        "PASSWORD": '',
        'HOST': 'sakchyam_db',
        'PORT': '5432'
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'sumit.naxa@gmail.com'
EMAIL_HOST_PASSWORD = 'sumit123#'
EMAIL_PORT = 587

