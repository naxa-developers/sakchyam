# Generated by Django 2.2.10 on 2020-06-16 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partnership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.IntegerField(blank=True, default=0, null=True)),
                ('blb', models.IntegerField(blank=True, default=0, null=True)),
                ('extension_counter', models.IntegerField(blank=True, default=0, null=True)),
                ('tablet', models.IntegerField(blank=True, default=0, null=True)),
                ('other_products', models.IntegerField(blank=True, default=0, null=True)),
                ('beneficiary', models.IntegerField(blank=True, default=0, null=True)),
                ('scf_funds', models.IntegerField(blank=True, default=0, null=True)),
                ('allocated_budget', models.FloatField(blank=True, default=0, null=True)),
                ('allocated_beneficiary', models.FloatField(blank=True, default=0, null=True)),
                ('female_percentage', models.FloatField(blank=True, default=0, null=True)),
                ('total_beneficiary', models.IntegerField(blank=True, default=0, null=True)),
                ('female_beneficiary', models.IntegerField(blank=True, default=0, null=True)),
                ('status', models.CharField(blank=True, max_length=500, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('project_year', models.CharField(blank=True, max_length=500, null=True)),
                ('district_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PartDistrict', to='api.District')),
                ('municipality_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PartMunicipality', to='api.Municipality')),
                ('partner_id', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PartnerPart', to='api.Partner')),
                ('project_id', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ProjectPartner', to='api.Project')),
                ('province_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PartProvince', to='api.Province')),
            ],
        ),
    ]
