# Generated by Django 4.2.13 on 2024-09-07 19:19

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('muhasebe', '0042_historicalurunler_stok_mu_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='urun_talepleri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miktar', models.FloatField(default=0, verbose_name='Taleb Adet Miktarı')),
                ('fiyati', models.FloatField(default=0, verbose_name='Fiyati')),
                ('tedarikci', models.CharField(blank=True, max_length=200, null=True, verbose_name='Tedarikçi')),
                ('aciklama', models.CharField(blank=True, max_length=500, null=True, verbose_name='Açıklama')),
                ('talep_Olusturma_tarihi', models.DateTimeField(blank=True, null=True, verbose_name='Talep Oluşturma Tarihi')),
                ('talep_durumu', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], default='1', max_length=3, verbose_name='Talep Durumu')),
                ('talep_durum_tarihi', models.DateTimeField(blank=True, null=True, verbose_name='Talep Durum Değiştirme Tarihi')),
                ('satin_alinma_durumu', models.BooleanField(default=False)),
                ('satin_alinma_tarihi', models.DateTimeField(blank=True, null=True, verbose_name='Satın Alınma Tarihi')),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('talebi_olusturan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='talebi_olusturan', to=settings.AUTH_USER_MODEL, verbose_name='Talebi Oluşturan')),
                ('talebin_ait_oldugu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='talebin_ait_oldugu', to=settings.AUTH_USER_MODEL, verbose_name='Talebin Ait Olduğu')),
                ('urun', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='muhasebe.urunler', verbose_name='Ürün')),
            ],
        ),
        migrations.CreateModel(
            name='Historicalurun_talepleri',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('miktar', models.FloatField(default=0, verbose_name='Taleb Adet Miktarı')),
                ('fiyati', models.FloatField(default=0, verbose_name='Fiyati')),
                ('tedarikci', models.CharField(blank=True, max_length=200, null=True, verbose_name='Tedarikçi')),
                ('aciklama', models.CharField(blank=True, max_length=500, null=True, verbose_name='Açıklama')),
                ('talep_Olusturma_tarihi', models.DateTimeField(blank=True, null=True, verbose_name='Talep Oluşturma Tarihi')),
                ('talep_durumu', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], default='1', max_length=3, verbose_name='Talep Durumu')),
                ('talep_durum_tarihi', models.DateTimeField(blank=True, null=True, verbose_name='Talep Durum Değiştirme Tarihi')),
                ('satin_alinma_durumu', models.BooleanField(default=False)),
                ('satin_alinma_tarihi', models.DateTimeField(blank=True, null=True, verbose_name='Satın Alınma Tarihi')),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('talebi_olusturan', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Talebi Oluşturan')),
                ('talebin_ait_oldugu', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Talebin Ait Olduğu')),
                ('urun', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='muhasebe.urunler', verbose_name='Ürün')),
            ],
            options={
                'verbose_name': 'historical urun_talepleri',
                'verbose_name_plural': 'historical urun_talepleris',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]