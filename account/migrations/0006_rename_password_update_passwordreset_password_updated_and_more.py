# Generated by Django 4.2.4 on 2023-08-08 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_passwordreset_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='passwordreset',
            old_name='password_update',
            new_name='password_updated',
        ),
        migrations.AddField(
            model_name='passwordreset',
            name='password',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
