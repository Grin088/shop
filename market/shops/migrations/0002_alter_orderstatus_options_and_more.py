# Generated by Django 4.2.1 on 2023-07-18 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("shops", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="orderstatus",
            options={
                "ordering": ["sort_index"],
                "verbose_name": "статус заказа",
                "verbose_name_plural": "статусы заказа",
            },
        ),
        migrations.AlterModelOptions(
            name="orderstatuschange",
            options={
                "ordering": ["-time"],
                "verbose_name": "изменение статуса заказа",
                "verbose_name_plural": "изменение статусов заказов",
            },
        ),
        migrations.RenameField(
            model_name="orderstatuschange",
            old_name="dst_status_id",
            new_name="dst_status",
        ),
        migrations.RenameField(
            model_name="orderstatuschange",
            old_name="src_status_id",
            new_name="src_status",
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="orders",
                to="shops.orderstatus",
                verbose_name="статус",
            ),
        ),
        migrations.AlterField(
            model_name="orderoffer",
            name="count",
            field=models.PositiveSmallIntegerField(verbose_name="количество"),
        ),
        migrations.CreateModel(
            name="PaymentQueue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("card_number", models.IntegerField(verbose_name="номер карты")),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shops.order",
                        verbose_name="заказ",
                    ),
                ),
            ],
        ),
    ]
