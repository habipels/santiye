# Generated by Django 4.2.13 on 2024-08-25 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0016_historicaltopbar_color_historicalsosyalmedyayoutube_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=40, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
