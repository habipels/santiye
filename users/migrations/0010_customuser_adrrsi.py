# Generated by Django 4.1.2 on 2024-06-14 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_personel_izinleri'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='adrrsi',
            field=models.TextField(blank=True, default='', max_length=600, verbose_name='Adres'),
        ),
    ]