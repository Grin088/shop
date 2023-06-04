from products.models import Review, Product


class ReviewServices:
    """Класс для обработки отзывов о товаре"""

    def __init__(self, request, product_id):
        self.product = Product.objects.get(id=product_id)
        self.user = request.user
        self.product_id = product_id
        self.reviews = Review.get_review(user_id=request.user.id, product_id=product_id)

    @classmethod
    def customer_can_write_review(cls, request, product_id):
        """Проверка может ли пользователь оставлять отзыв о товаре"""
        user = request.user

        order = user.orders.filter(
            status="paid", order_items__product_id=product_id
        ).last()

        return order

    def get_context(self, form):
        """Получение необходимого контекста для шаблона"""
        reviews_quantity = self.product.count_reviews()
        rating = round(self.product.average_rating(), 2)

        context = {
            "user": self.user,
            "product": self.product,
            "product_id": self.product_id,
            "form": form,
            "review_exist": self.reviews.first(),
            "reviews_quantity": reviews_quantity,
            "rating": rating,
            # "can_add_review": self.can_create_review()
        }

        return context

    def can_create_review(self):
        """Проверка возможности добавления отзыва пользователем"""
        return (
            self.customer.orders.filter(
                status="payed",
                order_items__product=self.product,
            ).exists()
            and not self.reviews
        )
