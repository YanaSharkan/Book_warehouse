# Generated by Django 4.1.7 on 2023-04-03 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0003_alter_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='brief_description',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='bookitem',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='warehouse.book'),
        ),
    ]
