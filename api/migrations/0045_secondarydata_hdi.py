# Generated by Django 2.2.10 on 2020-07-21 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_secondarydata'),
    ]

    operations = [
        migrations.AddField(
            model_name='secondarydata',
            name='hdi',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
