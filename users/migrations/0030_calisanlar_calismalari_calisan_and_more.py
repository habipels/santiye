# Generated by Django 4.2.13 on 2024-09-07 02:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0029_historicalcalisanlar_calismalari_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='calisanlar_calismalari',
            name='calisan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.calisanlar', verbose_name='Çalışan'),
        ),
        migrations.AddField(
            model_name='historicalcalisanlar_calismalari',
            name='calisan',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='users.calisanlar', verbose_name='Çalışan'),
        ),
    ]
