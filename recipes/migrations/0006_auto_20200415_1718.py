# Generated by Django 2.2.3 on 2020-04-15 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_planner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planner',
            name='date',
            field=models.DateField(),
        ),
    ]
