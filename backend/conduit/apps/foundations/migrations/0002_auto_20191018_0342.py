# Generated by Django 2.2.6 on 2019-10-18 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('foundations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='foundation',
            name='founder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='org', to='profiles.Profile'),
        ),
        migrations.AddField(
            model_name='foundation',
            name='grantees',
            field=models.ManyToManyField(related_name='foundations', to='profiles.Profile'),
        ),
        migrations.AddField(
            model_name='foundation',
            name='tags',
            field=models.ManyToManyField(related_name='foundations', to='foundations.Tag'),
        ),
    ]
