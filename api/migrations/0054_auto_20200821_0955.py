# Generated by Django 2.2.10 on 2020-08-21 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0053_auto_20200821_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='indirect_links',
            field=models.CharField(choices=[('RTGS', 'RTGS'), ('National Switch', 'National Switch'), ('CSD', 'CSD'), ('Card and Switch System', 'Card and Switch System'), ('PSPs/PSOs', 'PSPs/PSOs'), ('NCHL', 'NCHL'), ('BFIs', 'BFIs'), ('Capital Market Players', 'Capital Market Players')], default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='link_with_indirect',
            field=models.CharField(choices=[('RTGS', 'RTGS'), ('National Switch', 'National Switch'), ('CSD', 'CSD'), ('Card and Switch System', 'Card and Switch System'), ('PSPs/PSOs', 'PSPs/PSOs'), ('NCHL', 'NCHL'), ('BFIs', 'BFIs'), ('Capital Market Players', 'Capital Market Players')], default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='directlink',
            name='components',
            field=models.CharField(choices=[('RTGS', 'RTGS'), ('National Switch', 'National Switch'), ('CSD', 'CSD'), ('Card and Switch System', 'Card and Switch System'), ('PSPs/PSOs', 'PSPs/PSOs'), ('NCHL', 'NCHL'), ('BFIs', 'BFIs'), ('Capital Market Players', 'Capital Market Players')], max_length=500),
        ),
        migrations.AlterField(
            model_name='payment',
            name='component',
            field=models.CharField(choices=[('RTGS', 'RTGS'), ('National Switch', 'National Switch'), ('CSD', 'CSD'), ('Card and Switch System', 'Card and Switch System'), ('PSPs/PSOs', 'PSPs/PSOs'), ('NCHL', 'NCHL'), ('BFIs', 'BFIs'), ('Capital Market Players', 'Capital Market Players')], max_length=500),
        ),
    ]
