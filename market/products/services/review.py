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

