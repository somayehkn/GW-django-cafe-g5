# Generated by Django 5.0 on 2024-01-09 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_alter_customer_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_order',
            name='status',
            field=models.CharField(choices=[('Deliverd', 'Deliverd'), ('Confirmed', 'Confirmed'), ('Cooking', 'Cooking'), ('Ready delivery', 'Ready delivery'), ('Checked Out', 'Checked Out')], default='Confirmed', max_length=20),
        ),
    ]
