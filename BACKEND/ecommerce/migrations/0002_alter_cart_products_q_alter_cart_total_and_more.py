# Generated by Django 4.2.4 on 2023-10-04 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='products_q',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='productcart',
            name='subtotal',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]