# Generated by Django 4.2.13 on 2024-12-23 12:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('site_info', '0082_historicalteklif_icerikleri_birim_fiyati_ıqd_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalmusteri_notlari',
            name='musterisi',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='site_info.musteri_bilgisi', verbose_name='Müşterisi'),
        ),
        migrations.AlterField(
            model_name='musteri_notlari',
            name='musterisi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='site_info.musteri_bilgisi', verbose_name='Müşterisi'),
        ),
        migrations.CreateModel(
            name='Historicaldaire_evraklari',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('evrak_adi', models.CharField(blank=True, max_length=200, null=True, verbose_name='Evrak Adı')),
                ('evrak', models.TextField(blank=True, max_length=100, null=True, verbose_name='Evrak')),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('silinme_bilgisi', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('daire', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='site_info.daire_bilgisi', verbose_name='Daire')),
                ('evrak_kime_ait', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Proje Ait Olduğu')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical daire_evraklari',
                'verbose_name_plural': 'historical daire_evraklaris',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='daire_evraklari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evrak_adi', models.CharField(blank=True, max_length=200, null=True, verbose_name='Evrak Adı')),
                ('evrak', models.FileField(blank=True, null=True, upload_to='daire_evraklari/', verbose_name='Evrak')),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('silinme_bilgisi', models.BooleanField(default=False)),
                ('daire', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='site_info.daire_bilgisi', verbose_name='Daire')),
                ('evrak_kime_ait', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Proje Ait Olduğu')),
            ],
        ),
    ]
