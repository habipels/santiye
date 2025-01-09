from django.db import migrations, models
import datetime  # Tarih işlemleri için gerekli

class Migration(migrations.Migration):

    dependencies = [
        ('site_info', '0089_checkdaireleri_genel_notlar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalimalat_daire_balama',
            name='tamamlama_tarihi',
            field=models.DateField(blank=True, null=True, editable=False),
        ),
        migrations.AddField(
            model_name='imalat_daire_balama',
            name='tamamlama_tarihi',
            field=models.DateField(auto_now=True),
        ),
    ]
