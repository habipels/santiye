# Generated by Django 4.1.2 on 2023-12-30 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_info', '0017_taseronlar_telefon_numarasi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taseron_sozlesme_dosyalari',
            name='durum',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Durum'),
        ),
    ]
