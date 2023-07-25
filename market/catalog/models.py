from django.db import models
from django.utils.translation import gettext_lazy as _


class Catalog(models.Model):
    """Категории каталога"""

    name = models.CharField(max_length=100, help_text=_("наименование"))
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    image = models.FileField(upload_to="catalog/icon/", verbose_name=_("картинка"))
    is_featured = models.BooleanField(
        default=False, verbose_name=_("избранная категория")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("категория")
        verbose_name_plural = _("категории")
        ordering = [
            "name",
        ]
