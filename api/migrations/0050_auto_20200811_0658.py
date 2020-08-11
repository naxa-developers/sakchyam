# Generated by Django 2.2.10 on 2020-08-11 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0049_insurance'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='financial_literacy',
            field=models.CharField(blank=True, choices=[('Microfinance/Cooperative', 'Microfinance/Cooperative'), ('Commercial Banks and Mobile Network Operators', 'Commercial Banks and Mobile Network Operators'), ('Commercial Bank', 'Commercial Bank'), ('Microfinance', 'Microfinance'), ('Digital Financial Service Providers', 'Digital Financial Service Providers'), ('Cooperative', 'Cooperative'), ('Digital Financial Service Operator', 'Digital Financial Service Operator'), ('Insurance Provider', 'Insurance Provider'), ('Apex Organization', 'Apex Organization'), ('Mobile Network Operator', 'Mobile Network Operator'), ('Insurance', 'Insurance')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='partner',
            name='mfs',
            field=models.CharField(blank=True, choices=[('Microfinance/Cooperative', 'Microfinance/Cooperative'), ('Commercial Banks and Mobile Network Operators', 'Commercial Banks and Mobile Network Operators'), ('Commercial Bank', 'Commercial Bank'), ('Microfinance', 'Microfinance'), ('Digital Financial Service Providers', 'Digital Financial Service Providers'), ('Cooperative', 'Cooperative'), ('Digital Financial Service Operator', 'Digital Financial Service Operator'), ('Insurance Provider', 'Insurance Provider'), ('Apex Organization', 'Apex Organization'), ('Mobile Network Operator', 'Mobile Network Operator'), ('Insurance', 'Insurance')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='partner',
            name='outreach_expansion',
            field=models.CharField(blank=True, choices=[('Microfinance/Cooperative', 'Microfinance/Cooperative'), ('Commercial Banks and Mobile Network Operators', 'Commercial Banks and Mobile Network Operators'), ('Commercial Bank', 'Commercial Bank'), ('Microfinance', 'Microfinance'), ('Digital Financial Service Providers', 'Digital Financial Service Providers'), ('Cooperative', 'Cooperative'), ('Digital Financial Service Operator', 'Digital Financial Service Operator'), ('Insurance Provider', 'Insurance Provider'), ('Apex Organization', 'Apex Organization'), ('Mobile Network Operator', 'Mobile Network Operator'), ('Insurance', 'Insurance')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='partner',
            name='partnership',
            field=models.CharField(blank=True, choices=[('Microfinance/Cooperative', 'Microfinance/Cooperative'), ('Commercial Banks and Mobile Network Operators', 'Commercial Banks and Mobile Network Operators'), ('Commercial Bank', 'Commercial Bank'), ('Microfinance', 'Microfinance'), ('Digital Financial Service Providers', 'Digital Financial Service Providers'), ('Cooperative', 'Cooperative'), ('Digital Financial Service Operator', 'Digital Financial Service Operator'), ('Insurance Provider', 'Insurance Provider'), ('Apex Organization', 'Apex Organization'), ('Mobile Network Operator', 'Mobile Network Operator'), ('Insurance', 'Insurance')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='partner',
            name='product_process',
            field=models.CharField(blank=True, choices=[('Microfinance/Cooperative', 'Microfinance/Cooperative'), ('Commercial Banks and Mobile Network Operators', 'Commercial Banks and Mobile Network Operators'), ('Commercial Bank', 'Commercial Bank'), ('Microfinance', 'Microfinance'), ('Digital Financial Service Providers', 'Digital Financial Service Providers'), ('Cooperative', 'Cooperative'), ('Digital Financial Service Operator', 'Digital Financial Service Operator'), ('Insurance Provider', 'Insurance Provider'), ('Apex Organization', 'Apex Organization'), ('Mobile Network Operator', 'Mobile Network Operator'), ('Insurance', 'Insurance')], max_length=200, null=True),
        ),
    ]
