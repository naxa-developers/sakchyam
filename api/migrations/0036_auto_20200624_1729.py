# Generated by Django 2.2.10 on 2020-06-24 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_auto_20200617_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logdata',
            name='unit',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
