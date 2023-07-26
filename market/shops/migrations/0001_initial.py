# Generated by Django 4.2.1 on 2023-07-18 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=280, verbose_name='название баннера')),
                ('description', models.TextField(max_length=280, null=True, verbose_name='описание баннера')),
                ('image', models.ImageField(upload_to='media/banners/', verbose_name='изображение баннера')),
                ('active', models.BooleanField(default=True, verbose_name='статус активности баннера')),
            ],
            options={
                'verbose_name': 'баннер',
                'verbose_name_plural': 'баннеры',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена')),
                ('product_in_stock', models.BooleanField(default=True, verbose_name='товар в наличии')),
                ('free_shipping', models.BooleanField(default=False, verbose_name='бесплатная доставка')),
                ('date_of_creation', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('delivery', models.CharField(choices=[('ORDINARY', 'Обычная'), ('EXPRESS', 'Экспрес')], default='ORDINARY', max_length=8, verbose_name='доставка')),
                ('citi', models.CharField(max_length=100, verbose_name='город')),
                ('address', models.CharField(max_length=200, verbose_name='адрес')),
                ('pay', models.CharField(choices=[('ONLINE', 'Онлайн'), ('SOMEONE', 'Онлайн со случайного чужого счета')], default='ONLINE', max_length=8, verbose_name='доставка')),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.SmallIntegerField(verbose_name='количество')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_index', models.SmallIntegerField(unique=True, verbose_name='порядковый индекс')),
                ('name', models.CharField(max_length=100, verbose_name='статус заказа')),
            ],
            options={
                'verbose_name': 'статус заказа',
                'verbose_name_plural': 'статусы заказа',
            },
        ),
        migrations.CreateModel(
            name='OrderStatusChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='время изменения')),
            ],
            options={
                'verbose_name': 'изменение статуса заказа',
                'verbose_name_plural': 'изменение статусов заказов',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='название')),
                ('phone_number', models.CharField(max_length=13, verbose_name='номер телефона')),
                ('email', models.EmailField(max_length=100, verbose_name='почта')),
                ('products', models.ManyToManyField(related_name='shops', through='shops.Offer', to='products.product', verbose_name='товары в магазине')),
            ],
        ),
    ]
