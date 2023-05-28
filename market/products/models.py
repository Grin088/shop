from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg


def product_preview_directory_path(instance: "Product", filename: str) -> str:
    """Генерирует путь к картинке"""

    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Product(models.Model):
    """Продукт"""

    class Meta:
        verbose_name_plural = _("продукты")
        verbose_name = _("продукт")

    name = models.CharField(max_length=512, verbose_name=_("наименование"))
    preview = models.ImageField(
        null=True,
        blank=True,
        upload_to=product_preview_directory_path,
        verbose_name=_("предварительный просмотр"),
    )
    property = models.ManyToManyField(
        "Property", through="ProductProperty", verbose_name=_("характеристики")
    )

    def __str__(self):
        return self.name

    def count_reviews(self):
        """Вывод количества отзывов о продукте"""
        return Review.objects.filter(product=self).count()

    def average_rating(self):
        """Вывод средней оценки продукта"""
        return (
            Review.objects.filter(product=self)
            .aggregate(Avg("rating"))
            .get("rating__avg")
            or 0
        )


class Property(models.Model):
    """Свойство продукта"""

    class Meta:
        verbose_name_plural = _("свойства")
        verbose_name = _("свойство")

    name = models.CharField(max_length=512, verbose_name=_("наименование"))

    def __str__(self):
        return self.name


class ProductProperty(models.Model):
    """Значение свойства продукта"""

    class Meta:
        verbose_name_plural = _("свойства продуктов")
        verbose_name = _("свойство продукта")

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    property = models.ForeignKey(Property, on_delete=models.PROTECT)
    value = models.CharField(max_length=128, verbose_name=_("значение"))


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    """Генерирует путь к картинке"""

    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk, filename=filename
    )


class ProductImage(models.Model):
    class Meta:
        verbose_name_plural = _("изображение продукта")
        verbose_name = _("изображения продуктов")

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name=_("продукт")
    )
    image = models.ImageField(
        upload_to=product_images_directory_path, verbose_name=_("Изображение")
    )
    description = models.CharField(
        max_length=200, null=False, blank=True, verbose_name=_("Описание")
    )


class Review(models.Model):
    """Модель отзывов о товаре и его оценка"""

    customer = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, verbose_name=_("Покупатель")
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=_("Продукт")
    )
    # order = models.ForeignKey("Order", on_delete=models.DO_NOTHING, verbose_name=_("Заказ"))
    rating = models.PositiveSmallIntegerField(
        choices=((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"))
    )
    review_text = models.TextField(
        max_length=500, blank=True, null=True, verbose_name=_("Текст отзыва")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer, self.product, self.rating}"

    class Meta:
        unique_together = ("customer", "product")
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")

    def can_create_review(self):
        return (
            self.customer.orders.filter(
                status="delivered",
                order_items__product=self.product,
            ).exists()
            and not self.review_text
        )

    def can_edit_review(self):
        return (
            self.customer.orders.filter(
                status="delivered",
                order_items__product=self.product,
            ).exists()
            and self.review_text
        )
