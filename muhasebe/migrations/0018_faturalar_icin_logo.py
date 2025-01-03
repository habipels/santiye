# Generated by Django 4.1.2 on 2024-01-11 12:40

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('muhasebe', '0017_alter_gelir_odemesi_gelir_makbuzu_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='faturalar_icin_logo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gelir_makbuzu', models.FileField(blank=True, null=True, upload_to='faturalogosu/', verbose_name='Sayfaya Logo Light')),
                ('silinme_bilgisi', models.BooleanField(default=False)),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('gelir_kime_ait_oldugu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Gelir Ödemesi Kime Ait')),
            ],
        ),
    ]
