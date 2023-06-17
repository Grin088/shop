from django.test import TestCase
from django.core.management import call_command
from products.models import Import, Product # импортируем модели Import и Product


class ImportTestCase(TestCase):
    """класс для тестирования импорта данных"""

    def setUp(self):
        # метод для подготовки данных перед каждым тестом
        # создаем объект модели Import с именем файла для импорта
        self.import_obj = Import.objects.create(source='test_import.json')

    def test_import_data(self):
        """метод для проверки работы импорта данных"""

        # вызываем команду для запуска импорта с указанным именем файла
        call_command('import_data', self.import_obj.source)

        # получаем обновленный объект модели Import из базы данных
        self.import_obj.refresh_from_db()

        # проверяем, что статус импорта изменился на "Выполнен"
        self.assertEqual(self.import_obj.status, 'completed')

        # проверяем, что количество импортированных товаров равно 3
        self.assertEqual(self.import_obj.imported_count, 3)

        # проверяем, что список ошибок пустой
        self.assertFalse(self.import_obj.errors)

        # проверяем, что в базе данных появились товары из файла
        self.assertTrue(Product.objects.filter(name='Ноутбук ASUS VivoBook 15').exists())
        self.assertTrue(Product.objects.filter(name='Смартфон Samsung Galaxy S21').exists())
        self.assertTrue(Product.objects.filter(name='Планшет Apple iPad Air').exists())
