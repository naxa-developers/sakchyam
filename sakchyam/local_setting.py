DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'sakchyam_db',
        'USER': 'postgres',
        "PASSWORD": '',
        'HOST': '172.22.0.2',
        'PORT': '5432'
    }
}