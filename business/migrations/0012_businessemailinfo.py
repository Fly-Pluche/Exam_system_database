# Generated by Django 2.1 on 2022-07-07 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0011_delete_businessemailinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessEmailInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(db_index=True, default=True, help_text='状态', verbose_name='状态')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('email', models.CharField(blank=True, db_index=True, help_text='邮箱', max_length=40, null=True, unique=True, verbose_name='邮箱')),
            ],
            options={
                'verbose_name': '可认证企业',
                'verbose_name_plural': '可认证企业',
            },
        ),
    ]
