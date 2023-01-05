# Generated by Django 4.1.4 on 2022-12-31 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LittleLemonAPI', '0007_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='crew',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='crew', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.SmallIntegerField(),
        ),
        migrations.CreateModel(
            name='ItemOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='LittleLemonAPI.menuitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LittleLemonAPI.order')),
            ],
        ),
    ]