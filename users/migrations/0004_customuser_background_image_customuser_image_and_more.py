# Generated by Django 4.1.2 on 2023-12-26 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_kullanici_silme_bilgisi_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='background_image',
            field=models.ImageField(blank=True, null=True, upload_to='background/', verbose_name='background'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile/', verbose_name='Profile'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='sehir',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Şehir'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='telefon_numarasi',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefon Numarası '),
        ),
        migrations.AddField(
            model_name='customuser',
            name='ulke',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Ülke'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='zip_kod',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Zip Kodu'),
        ),
    ]
