# Generated by Django 4.2.13 on 2024-12-19 15:45

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('site_info', '0073_historicaltalep_ve_sikayet_daire_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='musteri_notlari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('not_basligi', models.CharField(blank=True, max_length=400, null=True, verbose_name='Not Başlığı')),
                ('not_aciklamasi', models.TextField()),
                ('not_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('kime_ait', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Proje Ait Olduğu')),
                ('musterisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='site_info.musteri_bilgisi', verbose_name='Müşeterisi')),
            ],
        ),
        migrations.CreateModel(
            name='Historicalmusteri_notlari',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('not_basligi', models.CharField(blank=True, max_length=400, null=True, verbose_name='Not Başlığı')),
                ('not_aciklamasi', models.TextField()),
                ('not_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('kime_ait', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Proje Ait Olduğu')),
                ('musterisi', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='site_info.musteri_bilgisi', verbose_name='Müşeterisi')),
            ],
            options={
                'verbose_name': 'historical musteri_notlari',
                'verbose_name_plural': 'historical musteri_notlaris',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]