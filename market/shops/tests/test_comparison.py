from django.test import TestCase
from shops.services.compare import (_adding_missing_properties,
                                    compare_list_check,
                                    )

#python manage.py test shops.tests.test_comparison.CompareTestCase
class CompareTestCase(TestCase):
    def setUpClass(cls):
        pass

    def test_compare_list_check_success(self):
        with self.settings(MAX_COMP_LIST_LEN=3):
            session = self.client.session
            for number_i in [1, 2, 2, 4, 5, 6, 5]:
                compare_list_check(session, number_i)
            expected_result = [1, 4]
            result = session.get("comp_list")
            self.assertEqual(result, expected_result)

    def test_splitting_into_groups_by_category(self):
        pass

    def test_adding_missing_properties_success(self):
        test_list = [{"property":{"Вес": ['5кг', False]}},
                     {"property":{"Высота": ['5кг', False]}},
                     {"property":{"Ширина": ['5кг', False]}},
                     ]
        test_list_property = ["Вес", "Высота", "Ширина"]
        expected_result = [{"property":{"Вес": ['5кг', False], "Высота": ['-', False], "Ширина": ['-', False]}},
                           {"property":{"Высота": ['5кг', False], "Вес": ['-', False], "Ширина": ['-', False]}},
                           {"property":{"Ширина": ['5кг', False], "Вес": ['-', False], "Высота": ['-', False]}},
                           ]
        result = _adding_missing_properties(test_list_property, test_list)
        self.assertEqual(result, expected_result)


