# from unittest.mock import patch
from django.test import TestCase
from products.models import Import, Product
from import_data.tasks import import_products


class ImportTestCase(TestCase):
    """класс для тестирования импорта данных"""

    def setUp(self):
        self.import_obj = Import.objects.create(source='import_test.json')

    def test_import_data(self):
        result = import_products(self.import_obj.source, 'test@example.com')
        self.assertEqual(result, f'Импорт из {self.import_obj.source} успешно завершен. Импортировано 2 товаров.')
        self.import_obj.refresh_from_db()
        self.assertEqual(self.import_obj.status, 'completed')
        self.assertEqual(self.import_obj.imported_count, 3)
        self.assertFalse(self.import_obj.errors)
        self.assertTrue(Product.objects.filter(name='Product 1').exists())
        self.assertTrue(Product.objects.filter(name='Product 2').exists())
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
