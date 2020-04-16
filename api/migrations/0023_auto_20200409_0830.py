# Generated by Django 2.2.10 on 2020-04-09 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20200408_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='municipality',
            name='district_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MunDistrict', to='api.District'),
        ),
        migrations.AlterField(
            model_name='municipality',
            name='province_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MunProvince', to='api.Province'),
        ),
        migrations.CreateModel(
            name='Automation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner_institution', models.CharField(blank=True, max_length=100, null=True)),
                ('branch', models.CharField(blank=True, max_length=100, null=True)),
                ('num_tablet_deployed', models.IntegerField(blank=True, default=0, null=True)),
                ('district_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AutoDistrict', to='api.District')),
                ('municipality_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AutoMunicipality', to='api.Municipality')),
                ('province_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AutoProvince', to='api.Province')),
            ],
        ),
    ]