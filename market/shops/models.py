from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Shop(models.Model):
    """Магазин"""
    name = models.CharField(max_length=512, verbose_name=_("название"))
    products = models.ManyToManyField("products.Product", through="Offer", related_name="shops",
                                      verbose_name=_("товары в магазине"))
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('пользователь'))
    phone_number = models.CharField(max_length=13, verbose_name=_('номер телефона'))
    email = models.EmailField(max_length=100, verbose_name=_('почта'))

    def __str__(self):
        return self.name


class Offer(models.Model):
    """Предложение магазина"""
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT)
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("цена"))


class Banner(models.Model):
    """Модель баннеров"""

    class Meta:
        verbose_name = _('баннер')
        verbose_name_plural = _('баннеры')

    title = models.CharField(max_length=280, verbose_name=_('название баннера'))
    description = models.TextField(max_length=280, null=True, verbose_name=_('описание баннера'))
    image = models.ImageField(upload_to='banners/',
                              verbose_name=_('изображение баннера'))
    link = models.URLField()
    start_date = models.DateTimeField(default=timezone.now, verbose_name=_('дата начала показа баннера'))
    end_date = models.DateTimeField(verbose_name=_('дата окончания показа баннера'))
    active = models.BooleanField(default=True, verbose_name=_('статус активности баннера'))

    def __str__(self):
        return self.title
