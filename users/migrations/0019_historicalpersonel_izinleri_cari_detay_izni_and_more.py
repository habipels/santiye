# Generated by Django 4.2.13 on 2024-08-30 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_historicalpersonel_izinleri_santiye_raporu_duzenleme_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpersonel_izinleri',
            name='cari_detay_izni',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalpersonel_izinleri',
            name='kasa_detay_izni',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personel_izinleri',
            name='cari_detay_izni',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personel_izinleri',
            name='kasa_detay_izni',
            field=models.BooleanField(default=False),
        ),
    ]