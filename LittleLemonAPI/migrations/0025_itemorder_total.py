# Generated by Django 4.1.4 on 2023-01-04 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0024_itemorder_quantity_alter_cart_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemorder',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=9),
            preserve_default=False,
        ),
    ]
