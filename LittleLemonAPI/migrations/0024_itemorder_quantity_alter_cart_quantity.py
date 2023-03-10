# Generated by Django 4.1.4 on 2023-01-04 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0023_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemorder',
            name='quantity',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.SmallIntegerField(),
        ),
    ]
