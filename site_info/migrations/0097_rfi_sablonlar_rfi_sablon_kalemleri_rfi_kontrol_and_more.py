# Generated by Django 4.2.13 on 2025-03-18 12:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('site_info', '0096_historicalimalat_daire_balama_dosya_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='rfi_sablonlar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfi_baslik', models.CharField(blank=True, max_length=200, null=True, verbose_name='RFI Başlık')),
                ('rfi_aciklama', models.TextField(blank=True, null=True, verbose_name='RFI Açıklama')),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('silinme_bilgisi', models.BooleanField(default=False)),
                ('olusturan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='olusturan', to=settings.AUTH_USER_MODEL, verbose_name='Oluşturan')),
                ('rfi_kime_ait', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Proje Ait Olduğu')),
                ('rfi_santiye', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='site_info.santiye', verbose_name='Santiye')),
            ],
        ),
        migrations.CreateModel(
            name='rfi_sablon_kalemleri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kalem_baslik', models.CharField(blank=True, max_length=200, null=True, verbose_name='Kalem Başlık')),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('silinme_bilgisi', models.BooleanField(default=False)),
                ('sablon_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='site_info.rfi_sablonlar', verbose_name='RFI Sablonu')),
            ],
        ),
        migrations.CreateModel(
            name='rfi_kontrol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kat_bilgisi', models.BigIntegerField(default=0, verbose_name='Kat Bİlgisi')),
                ('daire_no', models.BigIntegerField(default=0, verbose_name='Kat Bİlgisi')),
                ('mahal', models.CharField(max_length=400, verbose_name='Mahal')),
                ('file', models.FileField(blank=True, null=True, upload_to='rfi_dosyalari/', verbose_name='Dosya Adı')),
                ('onaylayan_tarih', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('onaylama_bilgisi', models.BooleanField(default=False)),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('silinme_bilgisi', models.BooleanField(default=False)),
                ('blok', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='site_info.bloglar', verbose_name='Proje bloglari')),
                ('onaylayan_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='onaylayan_bilgisi', to=settings.AUTH_USER_MODEL, verbose_name='Onaylayan')),
                ('sablon_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='site_info.rfi_sablonlar', verbose_name='RFI Sablonu')),
            ],
        ),
        migrations.CreateModel(
            name='Historicalrfi_sablonlar',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('rfi_baslik', models.CharField(blank=True, max_length=200, null=True, verbose_name='RFI Başlık')),
                ('rfi_aciklama', models.TextField(blank=True, null=True, verbose_name='RFI Açıklama')),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('silinme_bilgisi', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('olusturan', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Oluşturan')),
                ('rfi_kime_ait', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Proje Ait Olduğu')),
                ('rfi_santiye', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='site_info.santiye', verbose_name='Santiye')),
            ],
            options={
                'verbose_name': 'historical rfi_sablonlar',
                'verbose_name_plural': 'historical rfi_sablonlars',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Historicalrfi_sablon_kalemleri',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('kalem_baslik', models.CharField(blank=True, max_length=200, null=True, verbose_name='Kalem Başlık')),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('silinme_bilgisi', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('sablon_bilgisi', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='site_info.rfi_sablonlar', verbose_name='RFI Sablonu')),
            ],
            options={
                'verbose_name': 'historical rfi_sablon_kalemleri',
                'verbose_name_plural': 'historical rfi_sablon_kalemleris',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Historicalrfi_kontrol',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('kat_bilgisi', models.BigIntegerField(default=0, verbose_name='Kat Bİlgisi')),
                ('daire_no', models.BigIntegerField(default=0, verbose_name='Kat Bİlgisi')),
                ('mahal', models.CharField(max_length=400, verbose_name='Mahal')),
                ('file', models.TextField(blank=True, max_length=100, null=True, verbose_name='Dosya Adı')),
                ('onaylayan_tarih', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('onaylama_bilgisi', models.BooleanField(default=False)),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('silinme_bilgisi', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('blok', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='site_info.bloglar', verbose_name='Proje bloglari')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('onaylayan_bilgisi', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Onaylayan')),
                ('sablon_bilgisi', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='site_info.rfi_sablonlar', verbose_name='RFI Sablonu')),
            ],
            options={
                'verbose_name': 'historical rfi_kontrol',
                'verbose_name_plural': 'historical rfi_kontrols',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
