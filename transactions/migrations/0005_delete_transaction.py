# Generated by Django 5.0.6 on 2024-06-24 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_rename_user_account_transaction_account'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]