# Generated by Django 4.1.2 on 2024-06-15 04:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_info', '0031_alter_isplaniilerlemedosyalari_dosya_sahibi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='santiye',
            name='kat_sayisi',
        ),
        migrations.AddField(
            model_name='bloglar',
            name='kat_sayisi',
            field=models.FloatField(default=1, verbose_name='Kat Bilgisi'),
        ),
        migrations.AddField(
            model_name='santiye',
            name='baslangic_tarihi',
            field=models.DateTimeField(default=datetime.datetime.now, null=True),
        ),
        migrations.AddField(
            model_name='santiye',
            name='tahmini_bitis_tarihi',
            field=models.DateTimeField(default=datetime.datetime.now, null=True),
        ),
    ]
