# Generated by Django 4.2.13 on 2025-03-07 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_info', '0093_remove_historicalimalat_daire_balama_onaylama_notu_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='check_liste_onaylama_gruplari',
            name='tamamlanma_bilgisi',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalcheck_liste_onaylama_gruplari',
            name='tamamlanma_bilgisi',
            field=models.BooleanField(default=False),
        ),
    ]
