# Задача 23. Создание модели отзывов
# Создайте необходимые модели, связи, миграции и интеграции в админ-панель для отзывов к товарам на сайте.

# Задача 23.1. Разработка сервиса добавления отзывов
# Интегрируйте вёрстку блока «Отзывы» на детальной
# странице товара, для получения отзывов используйте сервис добавления отзывов.
# Также интегрируйте форму добавления отзыва, при добавлении отзыва вызывайте соответствующий метод сервиса.
# При возникновении ошибки валидации эти ошибки должны быть выведены над формой.
# При нажатии на ссылку «Показать ещё» должна быть осуществлена подгрузка отзывов.
# Кнопка должна скрыться, если уже загружены все отзывы.

# Реализуйте сервис добавления отзывов и все методы, доступные в нём:
# ●	добавить отзыв к товару,
# ●	получить список отзывов к товару,
# ●	получить количество отзывов для товара.
from products.models import Review


class ReviewHandler:

    def __init__(self, product_id):
        self.reviews = (
            Review.objects.select_related("customer")
            .select_related("product")
            .filter(product_id=product_id)
        )

    @classmethod
    def customer_can_write_review(cls, request, product_id):
        user = request.user
        order = user.orders.filter(
            status="paid", order_items__product_id=product_id
        ).last()

        return order

    def get_review(self):
        reviews = self.reviews
        reviews_quantity = reviews.count()
        if not reviews_quantity:
            return False
        elif reviews_quantity % 3 != 0:
            reviews_quantity += 3

        for i in range(3, reviews_quantity + 1, 3):
            yield reviews[:i]


# print(Review.objects.select_related('user').select_related('product').all())
