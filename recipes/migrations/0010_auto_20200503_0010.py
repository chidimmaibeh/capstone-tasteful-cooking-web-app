# Generated by Django 2.2.3 on 2020-05-03 05:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0009_remove_grocery_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='grocery',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='grocery',
            name='content',
            field=models.CharField(max_length=50),
        ),
    ]
