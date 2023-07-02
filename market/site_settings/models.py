from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _


class OneObjectModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(OneObjectModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class SiteSettings(OneObjectModel):
    """Модель настроек сайта"""

    # Пагинация
    pagination_size = models.PositiveIntegerField(validators=[MaxValueValidator(8)], default=8,
                                                  verbose_name='pagination size')
    # Главная страница
    banners_count = models.PositiveIntegerField(validators=[MaxValueValidator(3)], default=3,
                                                verbose_name='banners count')
    deal_of_the_day = models.PositiveIntegerField(validators=[MaxValueValidator(1)], default=1,
                                                  verbose_name='deal of the day quantity')
    hot_deals_slider = models.PositiveIntegerField(validators=[MaxValueValidator(9)], default=9,
                                                   verbose_name='hot deals slider')
    top_elements_count = models.PositiveIntegerField(validators=[MaxValueValidator(8)], default=8,
                                                     verbose_name='top elements count')
    limited_edition_count = models.PositiveIntegerField(validators=[MaxValueValidator(16)], default=16,
                                                        verbose_name='limited edition count')
    # Детальная страница товара
    maximum_number_of_viewed_products = models.PositiveIntegerField(validators=[MaxValueValidator(20)], default=20,
                                                                    verbose_name='maximum number of viewed products')
    # Способ доставки
    free_shipping_min_order_amount = models.DecimalField(max_digits=6, decimal_places=2, default=100.00,
                                                         verbose_name='free shipping min order amount, $')
    standard_shipping_price = models.DecimalField(max_digits=6, decimal_places=2, default=10.00,
                                                  verbose_name='standard shipping price, $')
    express_shipping_price = models.DecimalField(max_digits=6, decimal_places=2, default=25.00,
                                                 verbose_name='express shipping price, $')
    # Кэш
    cache_time = models.PositiveIntegerField(validators=[MaxValueValidator(3)], default=1,
                                             verbose_name='cache time, days')

    def __str__(self) -> str:
        return "Site settings"

    class Meta:
        verbose_name = _("настройка сайта")
        verbose_name_plural = _("настройки сайта")
