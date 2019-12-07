# Generated by Django 2.2.6 on 2019-12-01 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foundations', '0002_auto_20191125_0151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foundation',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='foundation',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]