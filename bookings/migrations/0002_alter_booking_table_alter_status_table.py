# Generated by Django 4.0.3 on 2022-04-13 01:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='booking',
            table='bookings',
        ),
        migrations.AlterModelTable(
            name='status',
            table='statuses',
        ),
    ]
