# Generated by Django 4.2.13 on 2024-09-01 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_info', '0045_remove_historicalprojeler_aciklama_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalprojeler',
            name='blog_bilgisi',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='site_info.bloglar'),
        ),
        migrations.AddField(
            model_name='historicalprojeler',
            name='kalem_bilgisi',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='site_info.santiye_kalemleri'),
        ),
        migrations.RemoveField(
            model_name='projeler',
            name='blog_bilgisi',
        ),
        migrations.RemoveField(
            model_name='projeler',
            name='kalem_bilgisi',
        ),
        migrations.AddField(
            model_name='projeler',
            name='blog_bilgisi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='site_info.bloglar'),
        ),
        migrations.AddField(
            model_name='projeler',
            name='kalem_bilgisi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='site_info.santiye_kalemleri'),
        ),
    ]