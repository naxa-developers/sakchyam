# Generated by Django 2.2.10 on 2020-03-18 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20200313_0810'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logcategory',
            old_name='description',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='logcategory',
            name='input',
        ),
        migrations.RemoveField(
            model_name='logdata',
            name='title',
        ),
        migrations.AddField(
            model_name='logsubcategory',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='logcategory',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='logsubcategory',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='milestoneyear',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='milestoneyear',
            name='range',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Title',
        ),
    ]