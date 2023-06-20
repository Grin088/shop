from django.db import models
from django.utils.translation import gettext_lazy as _


class Shop(models.Model):
    """Магазин"""
    name = models.CharField(max_length=512, verbose_name=_("название"))
    products = models.ManyToManyField("products.Product", through="Offer", related_name="shops",
                                      verbose_name=_("товары в магазине"))
    user = models.OneToOneField("users.CustomUser", on_delete=models.CASCADE, verbose_name=_('пользователь'))
    phone_number = models.CharField(max_length=13, verbose_name=_('номер телефона'))
    email = models.EmailField(max_length=100, verbose_name=_('почта'))

    def __str__(self):
        return self.name


class Offer(models.Model):
    """Предложение магазина"""
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT)
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT, related_name='offers')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("цена"))
    product_in_stock = models.BooleanField(default=True, verbose_name=_('товар в наличии'))
    free_shipping = models.BooleanField(default=False, verbose_name=_('бесплатная доставка'))


class Banner(models.Model):
    """Модель баннеров"""

    class Meta:
        verbose_name = _('баннер')
        verbose_name_plural = _('баннеры')

    title = models.CharField(max_length=280, verbose_name=_('название баннера'))
    description = models.TextField(max_length=280, null=True, verbose_name=_('описание баннера'))
    image = models.ImageField(upload_to='media/banners/',
                              verbose_name=_('изображение баннера'))

    active = models.BooleanField(default=True, verbose_name=_('статус активности баннера'))

    def __str__(self):
        return self.title
