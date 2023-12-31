# Generated by Django 4.1.2 on 2023-12-13 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('muhasebe', '0007_urunler'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gelir_bilgisi',
            name='adet',
        ),
        migrations.RemoveField(
            model_name='gelir_bilgisi',
            name='urun_adi',
        ),
        migrations.RemoveField(
            model_name='gider_bilgisi',
            name='adet',
        ),
        migrations.RemoveField(
            model_name='gider_bilgisi',
            name='urun_adi',
        ),
        migrations.RemoveField(
            model_name='urunler',
            name='virman_ait_oldugu',
        ),
        migrations.AddField(
            model_name='urunler',
            name='urun_ait_oldugu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='ürün Ait Olduğu'),
        ),
        migrations.CreateModel(
            name='gider_urun_bilgisi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urun_fiyati', models.FloatField(default=0, verbose_name='Ürün Fiyatı')),
                ('urun_adeti', models.FloatField(default=0, verbose_name='Ürün Adeti')),
                ('gider_bilgis', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='muhasebe.gider_bilgisi', verbose_name='Gider Bilgisi')),
                ('urun_ait_oldugu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Ürün Ait Olduğu')),
                ('urun_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='muhasebe.urunler', verbose_name='Ürün Bilgisi')),
            ],
        ),
        migrations.CreateModel(
            name='gelir_urun_bilgisi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urun_fiyati', models.FloatField(default=0, verbose_name='Ürün Fiyatı')),
                ('urun_adeti', models.FloatField(default=0, verbose_name='Ürün Adeti')),
                ('gider_bilgis', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='muhasebe.gelir_bilgisi', verbose_name='Gelir Bilgisi')),
                ('urun_ait_oldugu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Ürün Ait Olduğu')),
                ('urun_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='muhasebe.urunler', verbose_name='Ürün Bilgisi')),
            ],
        ),
    ]
