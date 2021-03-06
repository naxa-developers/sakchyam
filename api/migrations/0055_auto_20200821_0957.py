# Generated by Django 2.2.10 on 2020-08-21 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0054_auto_20200821_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='indirect_links',
            field=models.CharField(choices=[('RTGS', 'RTGS'), ('National Switch', 'National Switch'), ('CSD', 'CSD'), ('Card and Switch System', 'Card and Switch System'), ('PSPs/PSOs', 'PSPs/PSOs'), ('NCHL', 'NCHL'), ('BFIs', 'BFIs'), ('Capital Market Players', 'Capital Market Players')], default='null', max_length=500),
        ),
        migrations.AlterField(
            model_name='payment',
            name='link_with_indirect',
            field=models.CharField(choices=[('RTGS', 'RTGS'), ('National Switch', 'National Switch'), ('CSD', 'CSD'), ('Card and Switch System', 'Card and Switch System'), ('PSPs/PSOs', 'PSPs/PSOs'), ('NCHL', 'NCHL'), ('BFIs', 'BFIs'), ('Capital Market Players', 'Capital Market Players')], default='null', max_length=500),
        ),
    ]
