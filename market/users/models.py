from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


def user_avatar_directory_path(instance: User, filename: str) -> str:
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


@deconstructible
class EmailUniqueValidator:
    """Проверка уникальности адреса электронной почты"""

    def __call__(self, value):
        if User.objects.select_related('profile').filter(email=value).exists():
            raise ValidationError(f'Email {value} уже используется другим пользователем.')


class Profile(models.Model):
    """ Модель профиля пользователя"""

    phone_number_validator = PhoneNumberValidator()
    validate_image_size = ValidateImageSize()

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user')
    avatar = models.ImageField(
        null=False,
        blank=False,
        upload_to=user_avatar_directory_path,
        default=get_default_avatar_path,
        validators=[validators.validate_image_file_extension,
                    validate_image_size
                    ],
        help_text='Максимальный размер фала 2MB'
    )
    phone_number = models.CharField(max_length=20,
                                    verbose_name='phone number',
                                    help_text='Номер телефона должен начинаться с + и содержать только цифры',
                                    validators=[phone_number_validator,
                                                ],
                                    null=False,
                                    default='+0000000000'
                                    )

    def clean(self):
        """Валидация данных """
        super().clean()
        profile = Profile.objects.filter(phone_number=self.phone_number).exclude(id=self.id).first()
        if profile:
            exist_phone_number = profile.phone_number
            if exist_phone_number and exist_phone_number != '+0000000000':
                raise ValidationError(f'Пользователь с номером {exist_phone_number} уже существует.')

    @staticmethod
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        """ Создание профиля пользователя при создании нового пользователя """
        if created and not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)
        instance.profile.save()
