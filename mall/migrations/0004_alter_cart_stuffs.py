# Generated by Django 4.1.7 on 2023-03-27 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0003_cart_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='stuffs',
            field=models.ManyToManyField(to='mall.stuff'),
        ),
    ]