# Generated by Django 4.2.13 on 2024-09-08 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_calisanlar_calismalari_calisan_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpersonel_izinleri',
            name='satin_alma_talebi_duzenleme',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalpersonel_izinleri',
            name='satin_alma_talebi_gorme',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalpersonel_izinleri',
            name='satin_alma_talebi_olusturma',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalpersonel_izinleri',
            name='satin_alma_talebi_onaylama_duzenleme',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalpersonel_izinleri',
            name='satin_alma_talebi_onaylama_gorme',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalpersonel_izinleri',
            name='satin_alma_talebi_onaylama_olusturma',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalpersonel_izinleri',
            name='satin_alma_talebi_onaylama_silme',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalpersonel_izinleri',
            name='satin_alma_talebi_silme',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personel_izinleri',
            name='satin_alma_talebi_duzenleme',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personel_izinleri',
            name='satin_alma_talebi_gorme',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personel_izinleri',
            name='satin_alma_talebi_olusturma',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personel_izinleri',
            name='satin_alma_talebi_onaylama_duzenleme',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personel_izinleri',
            name='satin_alma_talebi_onaylama_gorme',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personel_izinleri',
            name='satin_alma_talebi_onaylama_olusturma',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personel_izinleri',
            name='satin_alma_talebi_onaylama_silme',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personel_izinleri',
            name='satin_alma_talebi_silme',
            field=models.BooleanField(default=False),
        ),
    ]