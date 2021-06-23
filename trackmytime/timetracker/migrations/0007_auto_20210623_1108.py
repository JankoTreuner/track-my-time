# Generated by Django 3.2.4 on 2021-06-23 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetracker', '0006_auto_20210622_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeentry',
            name='booked',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='timeentry',
            name='end',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
