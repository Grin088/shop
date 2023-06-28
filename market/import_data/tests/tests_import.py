# from unittest.mock import patch
from django.test import TestCase
from products.models import Import, Product
# from import_data.tasks import import_products
import json
import tempfile
from import_data.services import process_products


class ImportTestCase(TestCase):

    def setUp(self):
        # временный файл с данными для импорта
        self.import_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json')
        data = [
            {
                "name": "Product 1",
                "description": "Some description",
                "limited_edition": False,
                "preview": "https://example.com/image1.jpg",
                "category": "Category 1"
            },
            {
                "name": "Product 2",
                "description": "Another description",
                "limited_edition": True,
                "preview": "https://example.com/image2.jpg",
                "category": "Category 2"
            }
        ]
        json.dump(data, self.import_file)
        self.import_file.flush()

        # объект Import с источником из временного файла
        self.import_obj = Import.objects.create(source=self.import_file.name)

    def tearDown(self):
        # закрываем и удаляем временный файл
        self.import_file.close()

    def test_import_data(self):
        # вызываем функцию process_products и получаем список товаров и ошибок
        products, errors = process_products(self.import_obj.source)

        # проверяем, что список ошибок пустой
        self.assertFalse(errors)

        # проверяем, что длина списка товаров равна ожидаемому количеству импортированных товаров
        self.assertEqual(len(products), 2)

        # обновляем объект Import с новыми атрибутами и сохраняем его в базе данных
        self.import_obj.status = 'completed'
        self.import_obj.imported_count = len(products)
        self.import_obj.save()

        # получаем объект Import из базы данных и проверяем его атрибуты
        self.import_obj.refresh_from_db()
        self.assertEqual(self.import_obj.status, 'completed')
        self.assertEqual(self.import_obj.imported_count, 2)
        self.assertFalse(self.import_obj.errors)

        # проверяем, что товары с заданными именами существуют в базе данных
        self.assertTrue(Product.objects.filter(name='Product 1').exists())
        self.assertTrue(Product.objects.filter(name='Product 2').exists())

# class ImportTestCase(TestCase):
#     """класс для тестирования импорта данных"""
#
#     def setUp(self):
#         self.import_obj = Import.objects.create(source='import_test.json')
#
#     def test_import_data(self):
#         result = import_products(self.import_obj.source, 'test@example.com')
#         self.assertEqual(result, f'Импорт из {self.import_obj.source} успешно завершен. Импортировано 2 товаров.')
#         self.import_obj.refresh_from_db()
#         self.assertEqual(self.import_obj.status, 'completed')
#         self.assertEqual(self.import_obj.imported_count, 3)
#         self.assertFalse(self.import_obj.errors)
#         self.assertTrue(Product.objects.filter(name='Product 1').exists())
#         self.assertTrue(Product.objects.filter(name='Product 2').exists())
        # self.assertTrue(Product.objects.filter(name='Ноутбук ASUS VivoBook 15').exists())
        # self.assertTrue(Product.objects.filter(name='Смартфон Samsung Galaxy S21').exists())
        # self.assertTrue(Product.objects.filter(name='Планшет Apple iPad Air').exists())


# class TestImportProducts(TestCase):
#     def testimportproducts(self):
#         with open('testimport.json', 'w') as f:
#             f.write(
#                 '[{"name": "Product 1", "description": "Description 1",'
#                 ' "limitededition": false, "preview": "", "category": "Category 1"},'
#                 ' {"name": "Product 2", "description": "Description 2",'
#                 ' "limitededition": false, "preview": "", "category": "Category 1"}]')
#
#         with patch('django.core.mail.send_mail') as mocksendmail:
#             result = import_products.delay('testimport.json', 'test@example.com').get()
#
#         self.assertIn('Импорт из testimport.json успешно завершен. Импортировано 2 товаров.', result)
#         self.assertEqual(mocksendmail.callcount, 1)
#         self.assertEqual(mocksendmail.callargs[0][1],
#                          'Импорт товаров из файла testimport.json был успешно выполнен.'
#                          '\nПодробности импорта можно посмотреть в файле')
