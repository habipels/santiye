# Generated by Django 4.2.13 on 2024-11-10 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0048_historicalpersonel_izinleri_genel_rapor_duzenleme_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='imza_sifresi',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Onaylama Şifresi'),
        ),
        migrations.AddField(
            model_name='historicalcustomuser',
            name='imza_sifresi',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Onaylama Şifresi'),
        ),
    ]