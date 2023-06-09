# Generated by Django 4.1.7 on 2023-04-02 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookitem',
            old_name='book_id',
            new_name='book',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='order_id',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='orderitembookitem',
            old_name='book_item_id',
            new_name='book_item',
        ),
        migrations.RenameField(
            model_name='orderitembookitem',
            old_name='order_item_id',
            new_name='order_item',
        ),
    ]
