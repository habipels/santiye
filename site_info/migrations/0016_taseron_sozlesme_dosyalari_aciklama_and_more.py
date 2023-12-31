# Generated by Django 4.1.2 on 2023-12-30 01:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_info', '0015_cari_taseron_baglantisi'),
    ]

    operations = [
        migrations.AddField(
            model_name='taseron_sozlesme_dosyalari',
            name='aciklama',
            field=models.TextField(blank=True, null=True, verbose_name='Açıklama'),
        ),
        migrations.AddField(
            model_name='taseron_sozlesme_dosyalari',
            name='dosya_adi',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Sözleşme Adı'),
        ),
        migrations.AddField(
            model_name='taseron_sozlesme_dosyalari',
            name='durum',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Durum'),
        ),
        migrations.AddField(
            model_name='taseron_sozlesme_dosyalari',
            name='kayit_tarihi',
            field=models.DateTimeField(default=datetime.datetime.now, null=True),
        ),
        migrations.AddField(
            model_name='taseron_sozlesme_dosyalari',
            name='silinme_bilgisi',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='taseron_sozlesme_dosyalari',
            name='tarih',
            field=models.DateField(blank=True, null=True, verbose_name='Proje Tarihi'),
        ),
        migrations.AlterField(
            model_name='projeler',
            name='durum',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Durum'),
        ),
    ]
