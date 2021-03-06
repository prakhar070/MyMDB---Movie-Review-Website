# Generated by Django 2.0.5 on 2019-06-22 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20190622_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movieimage',
            name='image',
            field=models.ImageField(upload_to='images/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='movieimage',
            name='movie',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='movies.Movie'),
        ),
    ]
