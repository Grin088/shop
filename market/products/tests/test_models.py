from django.test import TestCase
from django.urls import reverse_lazy
from products.models import Product, Property, ProductProperty, Review
from users.models import CustomUser as User


class ProductModelTest(TestCase):
    """Класс тестов модели Продукт"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property = Property.objects.create(name="тестовая характеристика")
        cls.product = Product.objects.create(
            name="Тестовый продукт",
        )
        cls.product.property.set([cls.property])

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        ProductModelTest.property.delete()
        ProductModelTest.product.delete()

    def test_verbose_name(self):
        product = ProductModelTest.product
        field_verboses = {
            "name": "наименование",
            "property": "характеристики",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    product._meta.get_field(field).verbose_name, expected_value
                )

    def test_name_max_length(self):
        product = ProductModelTest.product
        max_length = product._meta.get_field("name").max_length
        self.assertEqual(max_length, 512)


class PropertyModelTest(TestCase):
    """Класс тестов модели Свойство продукта"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property = Property.objects.create(name="тестовая характеристика")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        PropertyModelTest.property.delete()

    def test_verbose_name(self):
        property = ProductModelTest.property
        field_verboses = {
            "name": "наименование",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    property._meta.get_field(field).verbose_name, expected_value
                )

    def test_name_max_length(self):
        property = ProductModelTest.property
        max_length = property._meta.get_field("name").max_length
        self.assertEqual(max_length, 512)


class ProductPropertyModelTest(TestCase):
    """Класс тестов модели Значение свойства продукта"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property = Property.objects.create(name="тестовая характеристика")
        cls.product = Product.objects.create(
            name="Тестовый продукт",
        )
        cls.product_property = ProductProperty.objects.create(
            product=cls.product,
            property=cls.property,
            value="тестовое значение характеристики",
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        ProductPropertyModelTest.product.delete()
        ProductPropertyModelTest.property.delete()
        ProductPropertyModelTest.product_property.delete()

    def test_verbose_name(self):
        product_property = ProductPropertyModelTest.product_property
        field_verboses = {
            "value": "значение",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    product_property._meta.get_field(field).verbose_name, expected_value
                )

    def test_value_max_length(self):
        product_property = ProductPropertyModelTest.product_property
        max_length = product_property._meta.get_field("value").max_length
        self.assertEqual(max_length, 128)


# class ProductReviewTest(TestCase):
#     """Класс тестов отзывов о товаре"""
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.user1 = User.objects.create_user(
#             email="test_user1@mail.ru", username="test_user1", password="123"
#         )
#         cls.user2 = User.objects.create_user(
#             email="test_user2@mail.ru", username="test_user2", password="123"
#         )
#         cls.user3 = User.objects.create_user(
#             email="test_user3@mail.ru", username="test_user3", password="123"
#         )
#         cls.user4 = User.objects.create_user(
#             email="test_user4@mail.ru", username="test_user4", password="123"
#         )
#         cls.user5 = User.objects.create_user(
#             email="test_user5@mail.ru", username="test_user5", password="123"
#         )
#         cls.user6 = User.objects.create_user(
#             email="test_user6@mail.ru", username="test_user6", password="123"
#         )
#         cls.product1 = Product.objects.create(name="product1")
#         cls.review1 = Review.objects.create(
#             user=cls.user1, product=cls.product1, rating=1, review_text="test text"
#         )
#         cls.review2 = Review.objects.create(
#             user=cls.user2, product=cls.product1, rating=2, review_text="test text"
#         )
#         cls.review3 = Review.objects.create(
#             user=cls.user3, product=cls.product1, rating=3, review_text="test text"
#         )
#         cls.review4 = Review.objects.create(
#             user=cls.user4, product=cls.product1, rating=4, review_text="test text"
#         )
#         cls.review5 = Review.objects.create(
#             user=cls.user5, product=cls.product1, rating=5, review_text="test text"
#         )
#
#     @classmethod
#     def tearDownClass(cls):
#         super().tearDownClass()
#         cls.user1.delete()
#         cls.user2.delete()
#         cls.user3.delete()
#         cls.user4.delete()
#         cls.user5.delete()
#         cls.user6.delete()
#         cls.review1.delete()
#         cls.review2.delete()
#         cls.review3.delete()
#         cls.review4.delete()
#         cls.review5.delete()
#         cls.product1.delete()
#
#     def test_view_reviews(self):
#         """Проверка страницы с отзывами"""
#         response = self.client.get(
#             reverse_lazy(
#                 "products:product_detail", kwargs={"product_id": self.product1.id}
#             )
#         )
#         self.assertEqual(response.status_code, 200)
#         #  проверка соответствия рейтинга и количества отзывов
#         self.assertContains(response, "Отзывы 5")
#         self.assertContains(response, "Средний рейтинг товара: 3.0")
#         login = self.client.login(username="test_user1@mail.ru", password="123")
#         self.assertTrue(login)
#         #  Пользователь, который оставил отзыв больше не может оставить отзыв о товаре.
#         self.assertNotContains(response, "Отправить отзыв")
#         self.client.logout()
#         self.client.login(username="test_user6@mail.ru", password="123")
#         response = self.client.get(
#             reverse_lazy(
#                 "products:product_detail", kwargs={"product_id": self.product1.id}
#             )
#         )
#         #  Проверка, что пользователь может отправить отзыв
#         self.assertContains(response, "Отправить отзыв")
#         self.client.logout()
#
#     def test_send_review(self):
#         """Проверка добавления отзыва о товаре"""
#         data = {"rating": 4, "review_text": "very good product !"}
#         login = self.client.login(username="test_user6@mail.ru", password="123")
#         self.assertTrue(login)
#         #  Проверка, что пользователь может отправить отзыв
#         response = self.client.get(
#             reverse_lazy(
#                 "products:product_detail", kwargs={"product_id": self.product1.id}
#             )
#         )
#         self.assertContains(response, "Отправить отзыв")
#         #  Проверка ошибки ввода данных
#         response = self.client.post(
#             reverse_lazy(
#                 "products:product_detail", kwargs={"product_id": self.product1.id}
#             )
#         )
#         self.assertContains(response, "error-message")
#         #  Проверка отправки отзыва
#         response = self.client.post(
#             reverse_lazy(
#                 "products:product_detail", kwargs={"product_id": self.product1.id}
#             ),
#             data=data,
#         )
#         self.assertEqual(response.status_code, 302)
#         #  Проверка добавления отзыва
#         response = self.client.get(
#             reverse_lazy(
#                 "products:product_detail", kwargs={"product_id": self.product1.id}
#             )
#         )
#         self.assertContains(response, "Средний рейтинг товара: 3.17")
#         self.assertContains(response, "Отзывы 6")
