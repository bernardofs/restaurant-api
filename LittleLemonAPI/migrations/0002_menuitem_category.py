# Generated by Django 4.1.4 on 2022-12-31 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='category',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]