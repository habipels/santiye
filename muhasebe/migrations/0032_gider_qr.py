# Generated by Django 4.1.2 on 2024-03-10 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('muhasebe', '0031_alter_gelir_qr_qr_bilgisi'),
    ]

    operations = [
        migrations.CreateModel(
            name='gider_qr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_bilgisi', models.ImageField(blank=True, null=True, upload_to='faturaqr/', verbose_name='Sayfaya Logo Light')),
                ('gelir_kime_ait_oldugu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='muhasebe.gider_bilgisi', verbose_name='Gelir Kategorisi Ait Olduğu')),
            ],
        ),
    ]