from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser



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


class OrderStatus(models.Model):
    """Модель статуса заказа"""

    class Meta:
        verbose_name = _('статус заказа')
        verbose_name_plural = _('статусы заказа')

    sort_index = models.SmallIntegerField(unique=True,  verbose_name=_('порядковый индекс'))
    name = models.CharField(max_length=100, verbose_name=_('статус заказа'))
    def __str__(self):
        return self.name


class Order(models.Model):
    """Модель заказов"""

    class Meta:
        verbose_name = _('заказ')
        verbose_name_plural = _('заказы')

    custom_user = models.ForeignKey(CustomUser,
                                    on_delete=models.PROTECT,
                                    related_name='orders',
                                    verbose_name=_('пользователь'))
    offer = models.ManyToManyField(Offer, through='OrderOffer',
                                   related_name='orders',
                                   verbose_name=_('предложение'))
    status = models.ForeignKey(OrderStatus,
                               on_delete=models.PROTECT,
                               related_name='orders',
                               verbose_name=_('статус'))
    data = models.DateTimeField(auto_now_add=True, verbose_name=_('дата создания'))


class OrderOffer(models.Model):
    """Промежуточная модель. Дополнительное поле количество товара"""

    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT)
    count = models.SmallIntegerField(verbose_name=_('количество'))


class OrderStatusChange(models.Model):
    """Модель сохранения хронологии изменения статуса заказа"""

    class Meta:
        verbose_name = _('изменение статуса заказа')
        verbose_name_plural = _('изменение статусов заказов')
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    time = models.DateTimeField(auto_now_add=True, verbose_name=_('время изменения'))
    src_status_id = models.ForeignKey(OrderStatus, related_name='orders_order_change_src', on_delete=models.PROTECT)
    dst_status_id = models.ForeignKey(OrderStatus, related_name='orders_order_change_dst', on_delete=models.PROTECT)
