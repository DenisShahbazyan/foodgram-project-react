# Generated by Django 4.0.3 on 2022-04-21 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_alter_amountingredientforrecipe_ingredient_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]
