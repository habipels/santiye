# Generated by Django 4.1.2 on 2023-12-29 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_info', '0012_projeler_kayit_tarihi'),
    ]

    operations = [
        migrations.AddField(
            model_name='projeler',
            name='silinme_bilgisi',
            field=models.BooleanField(default=False),
        ),
    ]