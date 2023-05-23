import re
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


def user_avatar_directory_path(instance, filename: str) -> str:
    """ Путь для сохранения аватара пользователя"""
    return f"users/avatars/user_{instance.pk}/{filename}"


def get_default_avatar_path():
    """ Путь к аватару пользователя по умолчанию"""
    return "users/avatars/default/default_avatar1.png"


@deconstructible
class PhoneNumberValidator(validators.RegexValidator):
    """Проверка формата номера телефона"""
    regex = r'^\+\d+$'
    message = 'Номер телефона должен начинаться с + и содержать только цифры'
    flags = 0


@deconstructible
class ValidateImageSize:
    """Проверка допустимого размера файла"""

    max_size = 2 * 1024 ** 2  # 2MB

    def __call__(self, image):
        if image.size > self.max_size:
            raise ValidationError('Размер файла превышает допустимое значение 2 MB.')


class CustomUserManager(UserManager):

    use_in_migrations = True

    @classmethod
    def validate_email(cls, email):
        """Проверка корректности ввода email"""
        regex = r'^[a-zA-Z0-9._]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email) is not None

    @classmethod
    def normalize_email(cls, email):
        """Перевод email в нижний регистр"""
        email = email or ""
        if cls.validate_email(email):
            email = email.lower()
            return email
        else:
            raise ValidationError(_('Enter validate email address'))


class CustomUser(AbstractUser):
    """Класс пользователя"""
    validate_image_size = ValidateImageSize()
    phone_number_validator = PhoneNumberValidator()

    objects = CustomUserManager()

    email = models.EmailField(
        _("email address"),
        blank=False,
        null=False,
        unique=True
    )
    avatar = models.ImageField(
        null=False,
        blank=False,
        upload_to=user_avatar_directory_path,
        default=get_default_avatar_path,
        validators=[
            validators.validate_image_file_extension,
            validate_image_size
           ],
        verbose_name=_("avatar")
    )
    phone_number = models.CharField(
        max_length=20,
        help_text='Номер телефона должен начинаться с + и содержать только цифры',
        validators=[phone_number_validator],
        null=False,
        default='+0000000000',
        verbose_name=_("phone number")
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def clean(self):
        """Валидация данных и проверка отсутствия номера телефона в базе данных"""
        super().clean()
        user = CustomUser.objects.filter(phone_number=self.phone_number).exclude(id=self.id).first()
        if user and user.phone_number != '+0000000000':
            raise ValidationError(f'Пользователь с номером {user.phone_number} уже существует.')

    class Meta:
        verbose_name = _("customer_user")
        verbose_name_plural = _("customer_users")
