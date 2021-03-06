# Generated by Django 3.0 on 2020-08-24 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('name', models.CharField(help_text='模块名称', max_length=200, unique=True, verbose_name='模块名称')),
                ('tester', models.CharField(help_text='测试人员', max_length=50, verbose_name='测试人员')),
                ('desc', models.CharField(blank=True, help_text='简要描述', max_length=200, null=True, verbose_name='简要描述')),
                ('project', models.ForeignKey(help_text='所属项目', on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='projects.Projects')),
            ],
            options={
                'verbose_name': '模块信息',
                'verbose_name_plural': '模块信息',
                'db_table': 'tb_modules',
            },
        ),
    ]
