# Generated by Django 5.1.2 on 2024-10-16 21:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0002_cases_bookmark_count_cases_comment_count_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cases',
            old_name='pub_date',
            new_name='date',
        ),
    ]
