# Generated by Django 4.0.4 on 2022-10-31 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='ton_adress',
        ),
        migrations.AddField(
            model_name='user',
            name='wallet_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='wallet_mnemonic',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='wallet_public_key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='wallet_secret_key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
