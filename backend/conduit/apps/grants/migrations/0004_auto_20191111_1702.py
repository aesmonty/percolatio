# Generated by Django 2.2.6 on 2019-11-11 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0003_auto_20191111_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grant',
            name='applicationsEndDate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='grant',
            name='applicationsStartDate',
            field=models.DateField(),
        ),
    ]
