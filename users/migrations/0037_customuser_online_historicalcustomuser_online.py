# Generated by Django 4.2.13 on 2024-09-18 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0036_historicalpersonel_izinleri_personeller_odeme_duzenleme_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='online',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalcustomuser',
            name='online',
            field=models.BooleanField(default=False),
        ),
    ]