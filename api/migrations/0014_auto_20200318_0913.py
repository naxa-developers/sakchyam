# Generated by Django 2.2.10 on 2020-03-18 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20200318_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logdata',
            name='achieved',
            field=models.CharField(blank=True, default=0, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='logdata',
            name='planned',
            field=models.CharField(blank=True, default=0, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='logdata',
            name='planned_afp',
            field=models.CharField(blank=True, default=0, max_length=30, null=True),
        ),
    ]