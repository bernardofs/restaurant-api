# Generated by Django 4.1.4 on 2022-12-31 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0004_alter_menuitem_price_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
