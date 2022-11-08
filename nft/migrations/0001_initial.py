# Generated by Django 4.0.4 on 2022-11-08 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryNFT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
            ],
            options={
                'verbose_name': 'NFT category',
                'verbose_name_plural': 'NFT categories',
            },
        ),
        migrations.CreateModel(
            name='CollectionNFT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/%Y/%m/%d/')),
                ('is_approved_to_sale', models.BooleanField(default=False)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'NFT collection',
                'verbose_name_plural': 'NFT collections',
            },
        ),
        migrations.CreateModel(
            name='DrawNFT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('finish_date', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'NFT draw',
                'verbose_name_plural': 'NFT draws',
            },
        ),
        migrations.CreateModel(
            name='NFT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=4, max_digits=19)),
                ('image', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('is_mint', models.BooleanField(default=False)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('index', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'NFT',
                'verbose_name_plural': 'NFT',
            },
        ),
        migrations.CreateModel(
            name='SaleNFT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('finish_date', models.DateTimeField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'NFT sale',
                'verbose_name_plural': 'NFT sales',
            },
        ),
    ]