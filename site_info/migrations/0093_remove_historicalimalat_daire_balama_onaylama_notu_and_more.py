# Generated by Django 4.2.13 on 2025-03-07 22:01

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('site_info', '0092_alter_historicalimalat_daire_balama_onaylma_tarihi_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalimalat_daire_balama',
            name='onaylama_notu',
        ),
        migrations.RemoveField(
            model_name='historicalimalat_daire_balama',
            name='onaylayan',
        ),
        migrations.RemoveField(
            model_name='historicalimalat_daire_balama',
            name='onaylma_tarihi',
        ),
        migrations.RemoveField(
            model_name='imalat_daire_balama',
            name='onaylama_notu',
        ),
        migrations.RemoveField(
            model_name='imalat_daire_balama',
            name='onaylayan',
        ),
        migrations.RemoveField(
            model_name='imalat_daire_balama',
            name='onaylma_tarihi',
        ),
        migrations.CreateModel(
            name='Historicalcheck_liste_onaylama_gruplari',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('onaylma_tarihi', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('onaylama_notu', models.TextField(blank=True, null=True)),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('imalat_kalemi_ait', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='site_info.imalat_daire_balama', verbose_name='İmalat Kalemi Ait Olduğu')),
                ('onaylayan', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Onaylayan')),
            ],
            options={
                'verbose_name': 'historical check_liste_onaylama_gruplari',
                'verbose_name_plural': 'historical check_liste_onaylama_gruplaris',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='check_liste_onaylama_gruplari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('onaylma_tarihi', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('onaylama_notu', models.TextField(blank=True, null=True)),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('imalat_kalemi_ait', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='site_info.imalat_daire_balama', verbose_name='İmalat Kalemi Ait Olduğu')),
                ('onaylayan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='onaylayan', to=settings.AUTH_USER_MODEL, verbose_name='Onaylayan')),
            ],
        ),
    ]
