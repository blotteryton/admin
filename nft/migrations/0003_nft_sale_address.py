# Generated by Django 4.0.4 on 2022-11-10 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nft', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nft',
            name='sale_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
