# Generated by Django 4.2.7 on 2023-12-31 09:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LittleLemonAPI', '0005_rename_menuitems_menuitem_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MenuItem',
            new_name='MenuItems',
        ),
        migrations.RenameModel(
            old_name='OrderItem',
            new_name='OrderItems',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='menuitem',
            new_name='menuitems',
        ),
        migrations.RenameField(
            model_name='orderitems',
            old_name='menuitem',
            new_name='menuitems',
        ),
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together={('user', 'menuitems')},
        ),
        migrations.AlterUniqueTogether(
            name='orderitems',
            unique_together={('order', 'menuitems')},
        ),
    ]
