# Generated by Django 4.2.13 on 2024-08-24 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muhasebe', '0038_rename_gelir_kategorisi_gelir_bilgisi_gelir_kategorisii_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gider_bilgisi',
            old_name='gelir_kategorisi',
            new_name='gelir_kategorisii',
        ),
        migrations.RenameField(
            model_name='historicalgider_bilgisi',
            old_name='gelir_kategorisi',
            new_name='gelir_kategorisii',
        ),
    ]