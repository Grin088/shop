from django.test import TestCase
from django.urls import reverse
from shops.services.compare import (_adding_missing_properties,
                                    compare_list_check,
                                    splitting_into_groups_by_category,
                                    _get_a_complete_list_of_property_names,
                                    _generating_a_comparison_dictionary,
                                    _comparison_of_product_properties,
                                    get_comparison_lists_and_properties,
                                    )


class CompareTestCase(TestCase):

    fixtures = {"fixtures/010_auth_group.json",
                "fixtures/011_users.json",
                "fixtures/015_shops_banner.json",
                "fixtures/020_catalog_categories.json",
                "fixtures/025_products.json",
                "fixtures/026_tags.json",
                "fixtures/027_product_image.json",
                "fixtures/030_property.json",
                "fixtures/035_productproperty.json",
                "fixtures/040_shops.json",
                "fixtures/045_offers.json",
                }

    def test_compare_list_check_success(self):
        with self.settings(MAX_COMP_LIST_LEN=3):
            session = self.client.session
            for number_i in [1, 2, 2, 4, 5, 6, 5]:
                compare_list_check(session, number_i)
            expected_result = [1, 4]
            result = session.get("comp_list")
            self.assertEqual(result, expected_result)

    def test_splitting_into_groups_by_category_success(self):
        comp_list = [1, 3, 4, 5, 17]
        result = splitting_into_groups_by_category(comp_list)
        expected_result = {"ноутбуки": [1, 3, 5, 4], "бытовая техника": [17]}
        self.assertEqual(result, expected_result)

    def test_get_a_complete_list_of_property_names_success(self):
        comp_list = [1, 3, 4, 5, 17]
        result = _get_a_complete_list_of_property_names(comp_list)
        expected_result = ['Вес',
                           'Гарантия от производителя',
                           'Страна-производитель',
                           'Цвет, заявленный производителем']
        self.assertEqual(result, expected_result)

    def test_generating_a_comparison_dictionary_success(self):
        comp_list = [1, 3]
        result = _generating_a_comparison_dictionary(comp_list)
        expected_result = [{'name': 'ноутбук 1',
                            'price': float(5000.00),
                            'preview': 'products/product_1/preview/bigGoods.png',
                            'id': 1,
                            'category': 'ноутбуки',
                            'property': {'Страна-производитель': ['Китай', False],
                                         'Гарантия от производителя': ['1', False],
                                         'Вес': ['5', False]}},
                           {'name': 'ноутбук 2',
                            'price': float(6000.00),
                            'preview': 'products/product_2/preview/card.jpg',
                            'id': 3,
                            'category': 'ноутбуки',
                            'property': {'Страна-производитель': ['Китай', False],
                                         'Гарантия от производителя': ['2', False]}}]

        self.assertEqual(result, expected_result)

    def test_adding_missing_properties_success(self):
        test_list = [{"property": {"Вес": ['5кг', False]}},
                     {"property": {"Высота": ['5кг', False]}},
                     {"property": {"Ширина": ['5кг', False]}},
                     ]
        test_list_property = ["Вес", "Высота", "Ширина"]
        expected_result = [{"property": {"Вес": ['5кг', False], "Высота": ['-', False], "Ширина": ['-', False]}},
                           {"property": {"Высота": ['5кг', False], "Вес": ['-', False], "Ширина": ['-', False]}},
                           {"property": {"Ширина": ['5кг', False], "Вес": ['-', False], "Высота": ['-', False]}},
                           ]
        result = _adding_missing_properties(test_list_property, test_list)
        self.assertEqual(result, expected_result)

    def test_comparison_of_product_properties_success(self):
        test_list = [{"property": {"Вес": ['5кг', False], "Высота": ['7 м', False], "Ширина": ['-', False]}},
                     {"property": {"Высота": ['7 м', False], "Вес": ['-', False], "Ширина": ['-', False]}},
                     {"property": {"Ширина": ['5кг', False], "Вес": ['-', False], "Высота": ['7 м', False]}},
                     ]
        test_list_property = ["Вес", "Высота", "Ширина"]
        result = _comparison_of_product_properties(test_list, test_list_property)
        expected_result = [{"property": {"Вес": ['5кг', False], "Высота": ['7 м', True], "Ширина": ['-', False]}},
                           {"property": {"Высота": ['7 м', True], "Вес": ['-', False], "Ширина": ['-', False]}},
                           {"property": {"Ширина": ['5кг', False], "Вес": ['-', False], "Высота": ['7 м', True]}},
                           ]
        self.assertEqual(result, expected_result)

    def test_get_comparison_lists_and_properties_success(self):
        comp_list = [1, 3]
        result_1, result_2 = get_comparison_lists_and_properties(comp_list)
        expected_result_1 = [{'name': 'ноутбук 1',
                              'price': float(50.00),
                              'preview': 'products/product_1/preview/bigGoods.png',
                              'id': 1,
                              'category': 'ноутбуки',
                              'property': {'Страна-производитель': ['Китай', True],
                                           'Гарантия от производителя': ['1', False],
                                           'Вес': ['5', False]}},
                             {'name': 'ноутбук 2',
                              'price': float(60.00),
                              'preview': 'products/product_2/preview/card.jpg',
                              'id': 3,
                              'category': 'ноутбуки',
                              'property': {'Страна-производитель': ['Китай', True],
                                           'Гарантия от производителя': ['2', False],
                                           'Вес': ['-', False]}}]
        expected_result_2 = ['Вес', 'Гарантия от производителя', 'Страна-производитель']
        print(result_1, expected_result_1)
        self.assertEqual(len(result_1), len(expected_result_1))
        self.assertEqual(result_2, expected_result_2)

    def test_compare_page_view_success(self):
        response = self.client.get(reverse("comparison"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Не достаточно данных для сравнения.")
