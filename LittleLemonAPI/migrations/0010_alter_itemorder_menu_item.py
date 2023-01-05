# Generated by Django 4.1.4 on 2023-01-01 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0009_alter_itemorder_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemorder',
            name='menu_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='menu_item', to='LittleLemonAPI.menuitem'),
        ),
    ]
