# Generated by Django 2.2.3 on 2020-05-03 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_grocery_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grocery',
            name='user',
        ),
    ]
