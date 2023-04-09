# Generated by Django 4.1.7 on 2023-04-08 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0005_alter_book_id_alter_bookitem_id_alter_order_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='book_store_id',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='book_item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='warehouse.bookitem'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='OrderItemBookItem',
        ),
    ]
