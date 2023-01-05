# Generated by Django 4.1.4 on 2023-01-02 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0011_alter_cart_menu_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemorder',
            name='menu_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='item_order_menu_item', to='LittleLemonAPI.menuitem'),
        ),
    ]