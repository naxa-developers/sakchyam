# Generated by Django 2.2.10 on 2020-06-17 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_partner_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='type',
            field=models.CharField(blank=True, choices=[('Microfinance Institutions/Cooperatives', 'Microfinance Institutions/Cooperatives'), ('Commercial Bank and Other Partners', 'Commercial Bank and Other Partners')], max_length=200, null=True),
        ),
    ]