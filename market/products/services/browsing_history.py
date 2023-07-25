from products.models import Browsing_history
import datetime


def is_valid_history(user_id, product_id):
    """Проверка на просмотр продукта"""
    try:
        update_date = Browsing_history.objects.get(
            users_id=user_id, product_id=product_id
        )
        update_date.data_at = datetime.datetime.now()
        update_date.save()
        return True
    except Browsing_history.DoesNotExist:
        return False


def browsing_history(user_id, product_id):
    """Добавление продукта в список просмотренных"""
    try:
        Browsing_history.objects.create(users_id=user_id, product_id=product_id)
    except Browsing_history.DoesNotExist:
        Browsing_history.objects.create(users_id=user_id, product_id=product_id)
