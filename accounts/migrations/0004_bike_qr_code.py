# Generated by Django 4.1.4 on 2022-12-27 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_order_bike'),
    ]

    operations = [
        migrations.AddField(
            model_name='bike',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes'),
        ),
    ]
