# Generated by Django 3.0 on 2020-06-19 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('debugtalks', '0003_auto_20200619_0937'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='debugtalks',
            name='project',
        ),
    ]
