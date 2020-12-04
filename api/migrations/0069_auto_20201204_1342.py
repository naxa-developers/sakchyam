# Generated by Django 2.2.10 on 2020-12-04 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0068_auto_20201204_0931'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='payment',
            name='component',
            field=models.CharField(blank=True, choices=[('RTGS', 'RTGS'), ('National Switch', 'National Switch'), ('CSD', 'CSD'), ('Card and Switch System', 'Card and Switch System'), ('PSPs/PSOs', 'PSPs/PSOs'), ('NCHL', 'NCHL'), ('BFIS', 'BFIS'), ('Capital Market Players', 'Capital Market Players')], max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='indirect_links',
            field=models.CharField(blank=True, choices=[('RTGS', 'RTGS'), ('National Switch', 'National Switch'), ('CSD', 'CSD'), ('Card and Switch System', 'Card and Switch System'), ('PSPs/PSOs', 'PSPs/PSOs'), ('NCHL', 'NCHL'), ('BFIS', 'BFIS'), ('Capital Market Players', 'Capital Market Players')], max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='link_with_indirect',
            field=models.CharField(blank=True, choices=[('RTGS', 'RTGS'), ('National Switch', 'National Switch'), ('CSD', 'CSD'), ('Card and Switch System', 'Card and Switch System'), ('PSPs/PSOs', 'PSPs/PSOs'), ('NCHL', 'NCHL'), ('BFIS', 'BFIS'), ('Capital Market Players', 'Capital Market Players')], max_length=500, null=True),
        ),
    ]
