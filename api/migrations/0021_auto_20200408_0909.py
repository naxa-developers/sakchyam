# Generated by Django 2.2.10 on 2020-04-08 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_milestoneyear_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logdata',
            name='data_type',
            field=models.CharField(blank=True, choices=[('number', 'Number'), ('budget', 'Budget'), ('percentage', 'Percentage')], max_length=30, null=True),
        ),
    ]
