# Generated by Django 2.2.3 on 2020-05-04 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_auto_20200503_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.CharField(max_length=1000, verbose_name='Directions'),
        ),
    ]
