# Generated by Django 4.2.13 on 2024-11-07 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_info', '0062_genel_rapor_raporu_olusturan_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='genel_rapor',
            name='silinme_bilgisi',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalgenel_rapor',
            name='silinme_bilgisi',
            field=models.BooleanField(default=False),
        ),
    ]
