# Generated by Django 4.0.4 on 2022-11-08 18:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_create_royalty', models.DecimalField(blank=True, decimal_places=4, max_digits=19, null=True, validators=[django.core.validators.MinValueValidator(0.0099)])),
                ('collection_create_royalty_address', models.CharField(blank=True, max_length=255, null=True)),
                ('collection_create_external_link', models.URLField(blank=True, null=True)),
                ('collection_create_seller_fee_basis_points', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(10000), django.core.validators.MinValueValidator(1)])),
                ('collection_create_fee_recipient', models.CharField(blank=True, help_text='use "self" for the address of the collection\'s creator.', max_length=255, null=True)),
                ('collection_create_amount', models.DecimalField(blank=True, decimal_places=4, max_digits=19, null=True, validators=[django.core.validators.MinValueValidator(0.0099)])),
                ('nft_create_amount', models.DecimalField(blank=True, decimal_places=4, max_digits=19, null=True, validators=[django.core.validators.MinValueValidator(0.0099)])),
                ('nft_item_content_base_uri', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Configuration',
                'verbose_name_plural': 'Configuration',
            },
        ),
        migrations.CreateModel(
            name='MarketplaceConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Marketplace configuration',
                'verbose_name_plural': 'Marketplace configuration',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('language', models.CharField(choices=[('RUSSIAN', '??????????????'), ('ENGLISH', 'English')], max_length=255)),
                ('channel_link', models.URLField(max_length=255)),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=255)),
                ('username', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=255)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='blogger_avatars/')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='blogger_covers/')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='administration.project')),
            ],
            options={
                'verbose_name': 'Project Member',
                'verbose_name_plural': 'Project Members',
            },
        ),
    ]
