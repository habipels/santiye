# Generated by Django 4.1.2 on 2023-12-30 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_customuser_sehir_remove_customuser_ulke_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='personel_dosyalari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dosyalari', models.FileField(blank=True, null=True, upload_to='kullanici_dosyasi/', verbose_name='Kullanıcı Dosyası')),
                ('kullanici', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı Bilgisi')),
            ],
        ),
    ]
