# Generated by Django 2.2.10 on 2020-08-21 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0055_auto_20200821_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='component',
            field=models.CharField(choices=[('null', 'null'), ('RTGS', 'RTGS'), ('National Switch', 'National Switch'), ('CSD', 'CSD'), ('Card and Switch System', 'Card and Switch System'), ('PSPs/PSOs', 'PSPs/PSOs'), ('NCHL', 'NCHL'), ('BFIS', 'BFIS'), ('Capital Market Players', 'Capital Market Players')], max_length=500),
        ),
        migrations.AlterField(
            model_name='payment',
            name='indirect_links',
            field=models.CharField(choices=[('null', 'null'), ('RTGS', 'RTGS'), ('National Switch', 'National Switch'), ('CSD', 'CSD'), ('Card and Switch System', 'Card and Switch System'), ('PSPs/PSOs', 'PSPs/PSOs'), ('NCHL', 'NCHL'), ('BFIS', 'BFIS'), ('Capital Market Players', 'Capital Market Players')], default='null', max_length=500),
        ),
        migrations.AlterField(
            model_name='payment',
            name='link_with_indirect',
            field=models.CharField(choices=[('null', 'null'), ('RTGS', 'RTGS'), ('National Switch', 'National Switch'), ('CSD', 'CSD'), ('Card and Switch System', 'Card and Switch System'), ('PSPs/PSOs', 'PSPs/PSOs'), ('NCHL', 'NCHL'), ('BFIS', 'BFIS'), ('Capital Market Players', 'Capital Market Players')], default='null', max_length=500),
        ),
        migrations.DeleteModel(
            name='DirectLink',
        ),
    ]
