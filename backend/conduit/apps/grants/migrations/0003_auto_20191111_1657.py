# Generated by Django 2.2.6 on 2019-11-11 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0002_auto_20191104_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grant',
            name='amountPerGrantee',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='grant',
            name='isPreFunded',
            field=models.BooleanField(default=False),
        ),
    ]