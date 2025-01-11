# Generated by Django 5.1.2 on 2025-01-11 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('seller_id', models.AutoField(primary_key=True, serialize=False)),
                ('owner_name', models.CharField(max_length=255)),
                ('shop_name', models.CharField(max_length=255)),
                ('shop_address', models.TextField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('IS_seller', models.BooleanField(default=True)),
            ],
        ),
    ]
