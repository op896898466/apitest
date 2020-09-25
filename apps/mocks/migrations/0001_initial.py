# Generated by Django 3.0 on 2020-08-24 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('interfacemocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mocks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('name', models.CharField(max_length=100, verbose_name='场景名称')),
                ('description', models.TextField(blank=True, verbose_name='简要描述')),
                ('enabled', models.BooleanField(blank=True, default=False, verbose_name='启用/禁用')),
                ('request', models.TextField(verbose_name='请求json')),
                ('response', models.TextField(verbose_name='响应json')),
                ('interfacemocks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mocks', to='interfacemocks.Interfacemocks')),
            ],
            options={
                'verbose_name': '接口名',
                'verbose_name_plural': '接口名',
                'db_table': 'tb_mocks',
            },
        ),
    ]
