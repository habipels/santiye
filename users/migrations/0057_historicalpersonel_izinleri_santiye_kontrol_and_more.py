# Generated by Django 4.2.13 on 2025-03-07 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0056_message_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpersonel_izinleri',
            name='santiye_kontrol',
            field=models.BooleanField(default=True, verbose_name='Santiye Kontrol'),
        ),
        migrations.AddField(
            model_name='personel_izinleri',
            name='santiye_kontrol',
            field=models.BooleanField(default=True, verbose_name='Santiye Kontrol'),
        ),
    ]
