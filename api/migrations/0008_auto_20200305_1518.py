# Generated by Django 2.2.10 on 2020-03-05 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20200305_1134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logdata',
            name='description',
        ),
        migrations.AddField(
            model_name='logsubcategory',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='title', to='api.LogSubCategory')),
            ],
        ),
        migrations.AddField(
            model_name='logdata',
            name='title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='LogData', to='api.Title'),
        ),
    ]
