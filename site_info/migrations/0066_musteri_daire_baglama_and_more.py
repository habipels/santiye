# Generated by Django 4.2.13 on 2024-11-26 15:36

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('site_info', '0065_musteri_bilgisi_historicalmusteri_bilgisi_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='musteri_daire_baglama',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('baglama_kime_ait', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='baglama_kime_ait', to=settings.AUTH_USER_MODEL, verbose_name='Proje Ait Olduğu')),
                ('daire', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='site_info.daire_bilgisi', verbose_name='Daire')),
                ('musterisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='site_info.musteri_bilgisi', verbose_name='Müşeterisi')),
            ],
        ),
        migrations.CreateModel(
            name='Historicalmusteri_daire_baglama',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('baglama_kime_ait', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Proje Ait Olduğu')),
                ('daire', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='site_info.daire_bilgisi', verbose_name='Daire')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('musterisi', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='site_info.musteri_bilgisi', verbose_name='Müşeterisi')),
            ],
            options={
                'verbose_name': 'historical musteri_daire_baglama',
                'verbose_name_plural': 'historical musteri_daire_baglamas',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]