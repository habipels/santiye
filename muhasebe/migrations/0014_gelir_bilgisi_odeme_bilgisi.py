# Generated by Django 4.1.2 on 2024-01-07 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muhasebe', '0013_alter_virman_virman_tarihi'),
    ]

    operations = [
        migrations.AddField(
            model_name='gelir_bilgisi',
            name='odeme_bilgisi',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Ödeme Bilgisi'),
        ),
    ]
