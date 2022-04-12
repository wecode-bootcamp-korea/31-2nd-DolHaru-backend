# Generated by Django 4.0.3 on 2022-04-12 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'amenities',
            },
        ),
        migrations.CreateModel(
            name='Highlight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'highlights',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'services',
            },
        ),
        migrations.CreateModel(
            name='Stay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bed', models.IntegerField(default=0)),
                ('bedroom', models.IntegerField(default=0)),
                ('bathroom', models.IntegerField(default=0)),
                ('guest_adult', models.IntegerField(default=0)),
                ('guest_kid', models.IntegerField(default=0)),
                ('guest_pet', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=400)),
                ('latitude', models.DecimalField(decimal_places=7, max_digits=11)),
                ('longitude', models.DecimalField(decimal_places=7, max_digits=11)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updatad_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'staies',
            },
        ),
        migrations.CreateModel(
            name='StayType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'stay_types',
            },
        ),
        migrations.CreateModel(
            name='StayService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staies.service')),
                ('stay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staies.stay')),
            ],
            options={
                'db_table': 'stay_services',
            },
        ),
        migrations.CreateModel(
            name='StayImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=4000)),
                ('stay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staies.stay')),
            ],
            options={
                'db_table': 'stay_images',
            },
        ),
        migrations.CreateModel(
            name='StayHighlight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('highlight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staies.highlight')),
                ('stay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staies.stay')),
            ],
            options={
                'db_table': 'stay_highlights',
            },
        ),
        migrations.CreateModel(
            name='StayAmenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staies.amenity')),
                ('stay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staies.stay')),
            ],
            options={
                'db_table': 'stay_amenities',
            },
        ),
        migrations.AddField(
            model_name='stay',
            name='amenities',
            field=models.ManyToManyField(through='staies.StayAmenity', to='staies.amenity'),
        ),
        migrations.AddField(
            model_name='stay',
            name='highlight',
            field=models.ManyToManyField(through='staies.StayHighlight', to='staies.highlight'),
        ),
        migrations.AddField(
            model_name='stay',
            name='services',
            field=models.ManyToManyField(through='staies.StayService', to='staies.service'),
        ),
        migrations.AddField(
            model_name='stay',
            name='stay_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staies.staytype'),
        ),
        migrations.AddField(
            model_name='stay',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
    ]
