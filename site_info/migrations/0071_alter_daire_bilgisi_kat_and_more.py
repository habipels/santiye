# Generated by Django 4.2.13 on 2024-12-13 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_info', '0070_historicalmusteri_bilgisi_musteri_telefon_numarasi_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daire_bilgisi',
            name='kat',
            field=models.IntegerField(default=1, verbose_name='Kat Bilgisi'),
        ),
        migrations.AlterField(
            model_name='historicaldaire_bilgisi',
            name='kat',
            field=models.IntegerField(default=1, verbose_name='Kat Bilgisi'),
        ),
    ]
