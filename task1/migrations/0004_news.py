# Generated by Django 5.1.4 on 2024-12-16 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task1', '0003_delete_user_buyer_registration_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]