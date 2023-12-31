# Generated by Django 4.1.2 on 2023-12-13 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('muhasebe', '0003_gider_kategorisi_gelir_kategorisi'),
    ]

    operations = [
        migrations.CreateModel(
            name='gider_etiketi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gider_etiketi_adi', models.CharField(blank=True, max_length=400, null=True, verbose_name='Gider Adı')),
                ('silinme_bilgisi', models.BooleanField(default=False)),
                ('gider_kategoris_ait_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Gider Kategorisi Ait Olduğu')),
            ],
        ),
        migrations.CreateModel(
            name='gelir_etiketi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gelir_etiketi_adi', models.CharField(blank=True, max_length=400, null=True, verbose_name='Gelir Adı')),
                ('silinme_bilgisi', models.BooleanField(default=False)),
                ('gelir_kategoris_ait_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Gelir Kategorisi Ait Olduğu')),
            ],
        ),
        migrations.CreateModel(
            name='Gelir_Bilgisi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fatura_tarihi', models.DateTimeField(blank=True, null=True, verbose_name='Fatura Tarihi')),
                ('fatura_no', models.CharField(blank=True, max_length=200, null=True, verbose_name='Fatura No')),
                ('aciklama', models.TextField(blank=True, null=True, verbose_name='Gelir Açıklaması')),
                ('urun_adi', models.CharField(blank=True, max_length=200, null=True, verbose_name='Ürün Adı')),
                ('adet', models.FloatField(default=1, verbose_name='Ürün Adeti')),
                ('tutar', models.FloatField(default=0, verbose_name='Toplam Tutar')),
                ('cari_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='muhasebe.cari', verbose_name='Cari Bilgisi')),
                ('gelir_etiketi_sec', models.ManyToManyField(blank=True, null=True, to='muhasebe.gelir_etiketi')),
                ('gelir_kategorisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='muhasebe.gelir_kategorisi', verbose_name='Gelirin Kategori Bilgisi')),
                ('gelir_kime_ait_oldugu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Gider Kategorisi Ait Olduğu')),
            ],
        ),
    ]
