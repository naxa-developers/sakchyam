# Generated by Django 2.2.10 on 2020-05-17 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20200517_0619'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='n_code',
            field=models.IntegerField(default=0),
        ),
    ]