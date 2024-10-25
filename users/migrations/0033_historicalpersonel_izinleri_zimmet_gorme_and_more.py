# Generated by Django 4.2.13 on 2024-09-10 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0032_historicalpersonel_izinleri_stok_olusturma_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpersonel_izinleri',
            name='zimmet_gorme',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalpersonel_izinleri',
            name='zimmet_olusturma',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalpersonel_izinleri',
            name='zimmet_silme',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personel_izinleri',
            name='zimmet_gorme',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personel_izinleri',
            name='zimmet_olusturma',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personel_izinleri',
            name='zimmet_silme',
            field=models.BooleanField(default=False),
        ),
    ]
