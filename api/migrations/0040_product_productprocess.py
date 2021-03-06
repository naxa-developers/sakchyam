# Generated by Django 2.2.10 on 2020-07-01 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_project_scf_funds'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('product_type', models.CharField(blank=True, max_length=500, null=True)),
                ('code', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner_type', models.CharField(blank=True, max_length=500, null=True)),
                ('product', models.CharField(blank=True, max_length=500, null=True)),
                ('product_category', models.CharField(blank=True, max_length=500, null=True)),
                ('innovation_area', models.CharField(blank=True, max_length=500, null=True)),
                ('market_failure', models.CharField(blank=True, max_length=500, null=True)),
                ('partner_id', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ProcessProduct', to='api.Partner')),
                ('product_id', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ProcessProduct', to='api.Product')),
            ],
        ),
    ]
