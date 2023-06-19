from products.models import Review, Product


class ProductsServices:
    """Класс для обработки отзывов о товаре"""

    def __init__(self, request, product_id):
        self.product = Product.objects.get(id=product_id)
        self.user = request.user
        self.product_id = product_id
        self.reviews = Review.get_review(user_id=request.user.id, product_id=product_id)
        self.images = self.product.product_images.all()

    @classmethod
    def customer_can_write_review(cls, request, product_id):
        """Проверка возможности добавления отзыва пользователем"""

        user = request.user

        order = user.orders.filter(
            status="paid", order_items__product_id=product_id
        ).last()

        return order

    def get_context(self, form):
        """Получение необходимого контекста для шаблона"""
        reviews_quantity = self.product.get_count_reviews()
        rating = round(self.product.get_average_rating(), 2)

        context = {
            "user": self.user,
            "product": self.product,
            "product_id": self.product_id,
            "form": form,
            "review_exist": self.reviews.first(),
            "reviews_quantity": reviews_quantity,
            "rating": rating,
            "images": self.images,
            # "can_add_review": self.customer_can_write_review()
        }

        return context
