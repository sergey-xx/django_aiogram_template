# Generated by Django 5.0.6 on 2024-06-18 09:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('status', models.CharField(max_length=20, verbose_name='Статус')),
                ('paid', models.BooleanField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Размер платежа')),
                ('currency', models.CharField(max_length=4, verbose_name='Валюта')),
                ('description', models.CharField(max_length=100, verbose_name='Описание')),
                ('confirm_url', models.URLField(verbose_name='Ссылка на Юкассу')),
                ('created_at', models.DateTimeField()),
                ('paid_at', models.DateTimeField(blank=True, null=True)),
                ('tg_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment', to='users.tguser', verbose_name='Пользователь телеграм')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('payment_type', models.CharField(max_length=50, verbose_name='Тип')),
                ('saved', models.BooleanField()),
                ('title', models.CharField(max_length=100, verbose_name='Название платежного метода')),
                ('card_first6', models.CharField(max_length=6, verbose_name='Первые 6 цифр карты')),
                ('card_last4', models.CharField(max_length=6, verbose_name='Последние 4 цифры карты')),
                ('expiry_year', models.CharField(max_length=4, verbose_name='Год экспирации')),
                ('expiry_month', models.CharField(max_length=2, verbose_name='Месяц экспирации')),
                ('card_type', models.CharField(max_length=50, verbose_name='Тип карты')),
                ('tg_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment_method', to='users.tguser', verbose_name='Пользователь телеграм')),
            ],
            options={
                'verbose_name': 'Платежный метод',
                'verbose_name_plural': 'Платежные методы',
            },
        ),
    ]