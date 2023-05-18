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


def phone_unique_validator(value):
    """Проверка уникальности номера телефона """
    user = User.objects.select_related('profile').filter(profile__phone_number=value).exists()
    if user and value != '+0000000000':
        raise ValidationError('%s уже используется другим пользователем.' % value)


def validate_image_size(image):
    """Проверка допустимого размера файла"""
    MAX_SIZE = 2 * 1024 ** 2  # 2MB
    if image.size > MAX_SIZE:
        raise ValidationError('Размер файла превышает допустимое значение 2 MB.')


class Profile(models.Model):
    """ Модель профиля пользователя"""
    phone_number_validator = PhoneNumberValidator()
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
                                    error_messages={'unique': 'Данный номер уже зарегистрирован'},
                                    validators=[phone_number_validator,
                                                phone_unique_validator
                                                ],
                                    null=False,
                                    default='+0000000000'
                                    )

    class Meta:
        verbose_name = 'User profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ Создание профиля пользователя при создании нового пользователя """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохранение профиля пользователя """
    instance.profile.save()
