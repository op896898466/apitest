# Generated by Django 3.0 on 2020-09-16 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testcases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcases',
            name='files',
            field=models.TextField(default='[]', help_text='文件信息', verbose_name='文件信息'),
        ),
    ]
