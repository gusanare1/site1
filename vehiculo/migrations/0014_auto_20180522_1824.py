# Generated by Django 2.0.5 on 2018-05-22 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculo', '0013_auto_20180522_0048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='apellido',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='nombre',
        ),
        migrations.AddField(
            model_name='persona',
            name='username',
            field=models.CharField(default='', max_length=30),
        ),
    ]
