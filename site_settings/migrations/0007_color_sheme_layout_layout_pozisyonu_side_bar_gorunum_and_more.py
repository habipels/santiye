# Generated by Django 4.1.2 on 2024-01-15 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0006_faturalardaki_gelir_gider_etiketi'),
    ]

    operations = [
        migrations.CreateModel(
            name='color_sheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=500, verbose_name='Görünüş isimleri')),
                ('data_bs_theme', models.CharField(max_length=500, verbose_name='Görünüş Anahtarı')),
                ('aktiflik', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='layout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=500, verbose_name='Görünüş isimleri')),
                ('data_layout', models.CharField(max_length=500, verbose_name='Görünüş Anahtarı')),
                ('aktiflik', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='layout_pozisyonu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=500, verbose_name='Görünüş isimleri')),
                ('data_layout_position', models.CharField(max_length=500, verbose_name='Görünüş Anahtarı')),
                ('aktiflik', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='side_bar_gorunum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=500, verbose_name='Görünüş isimleri')),
                ('data_sidebar_visibility', models.CharField(max_length=500, verbose_name='Görünüş Anahtarı')),
                ('aktiflik', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='sidebar_boyutu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=500, verbose_name='Görünüş isimleri')),
                ('data_sidebar_size', models.CharField(max_length=500, verbose_name='Görünüş Anahtarı')),
                ('aktiflik', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='sidebar_rengi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=500, verbose_name='Görünüş isimleri')),
                ('data_sidebar', models.CharField(max_length=500, verbose_name='Görünüş Anahtarı')),
                ('aktiflik', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='topbar_color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=500, verbose_name='Görünüş isimleri')),
                ('data_topbar', models.CharField(max_length=500, verbose_name='Görünüş Anahtarı')),
                ('aktiflik', models.BooleanField(default=False)),
            ],
        ),
    ]