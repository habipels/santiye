# Generated by Django 4.2.13 on 2024-09-06 02:17

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_calisanlar_calismalari_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historicalcalisanlar_pozisyonu',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('kategori_isimi', models.CharField(max_length=200, verbose_name='Çalışan Kategori İsmi')),
                ('silinme_bilgisi', models.BooleanField(default=False)),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('kategori_kime_ait', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Çalışan Kime Ait')),
            ],
            options={
                'verbose_name': 'historical calisanlar_pozisyonu',
                'verbose_name_plural': 'historical calisanlar_pozisyonus',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='calisanlar_pozisyonu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kategori_isimi', models.CharField(max_length=200, verbose_name='Çalışan Kategori İsmi')),
                ('silinme_bilgisi', models.BooleanField(default=False)),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('kategori_kime_ait', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Çalışan Kime Ait')),
            ],
        ),
        migrations.AddField(
            model_name='calisanlar',
            name='calisan_pozisyonu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.calisanlar_pozisyonu', verbose_name='Çalışan Kategorisi'),
        ),
        migrations.AddField(
            model_name='historicalcalisanlar',
            name='calisan_pozisyonu',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='users.calisanlar_pozisyonu', verbose_name='Çalışan Kategorisi'),
        ),
    ]