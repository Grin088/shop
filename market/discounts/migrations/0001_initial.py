# Generated by Django 4.2.1 on 2023-07-17 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItemDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='название скидки')),
                ('description', models.TextField(max_length=150, verbose_name='описание скидки')),
                ('discount_amount', models.PositiveIntegerField(verbose_name='размер скидки')),
                ('discount_amount_type', models.PositiveSmallIntegerField(choices=[(1, 'проценты'), (2, 'сумма')])),
                ('active', models.BooleanField(verbose_name='скидка активна')),
                ('start_date', models.DateTimeField(verbose_name='дата начала действия скидки')),
                ('end_date', models.DateTimeField(verbose_name='дата окончания действия скидки')),
                ('min_total_price_of_cart', models.DecimalField(blank=True, decimal_places=2, help_text='скидка может быть установлена на стоимость товаров в корзине.', max_digits=10, null=True, verbose_name='минимальная цена товаров в корзине')),
                ('max_total_price_of_cart', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='максимальная цена товаров в корзине')),
                ('min_amount_product_in_cart', models.PositiveIntegerField(blank=True, help_text='скидка может быть установлена на количество товаров в корзине.', null=True, verbose_name='минимальное количество товаров в корзине')),
                ('max_amount_product_in_cart', models.PositiveIntegerField(blank=True, null=True, verbose_name='максимальное количество товаров в корзине')),
            ],
            options={
                'verbose_name': 'скидка на товар в корзине',
                'verbose_name_plural': 'скидки на товары в корзине',
            },
        ),
        migrations.CreateModel(
            name='ShopItemDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='название скидки')),
                ('description', models.TextField(max_length=150, verbose_name='описание скидки')),
                ('discount_amount', models.PositiveIntegerField(verbose_name='размер скидки')),
                ('discount_amount_type', models.PositiveSmallIntegerField(choices=[(1, 'проценты'), (2, 'сумма')])),
                ('active', models.BooleanField(verbose_name='скидка активна')),
                ('start_date', models.DateTimeField(verbose_name='дата начала действия скидки')),
                ('end_date', models.DateTimeField(verbose_name='дата окончания действия скидки')),
                ('categories', models.ManyToManyField(blank=True, related_name='shop_items_discounts', to='catalog.catalog', verbose_name='категории товаров')),
            ],
            options={
                'verbose_name': 'скидка на товар в магазине',
                'verbose_name_plural': 'скидки на товары в магазине',
            },
        ),
    ]
