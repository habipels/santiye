# Generated by Django 4.2.13 on 2025-03-19 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_info', '0099_historicalrfi_kontrol_kontrol_ekleyen_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalrfi_kontrol',
            name='red_sebebi',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Red Sebebi'),
        ),
        migrations.AddField(
            model_name='rfi_kontrol',
            name='red_sebebi',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Red Sebebi'),
        ),
    ]
