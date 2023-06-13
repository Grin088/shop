from products.models import Browsing_history


def is_valid_history(user_id, product_id):
    """Проверка на просмотр продукта"""
    print('Идет проверка')
    try:
        Browsing_history.objects.get(users_id=user_id,
                                     product_id=product_id)
        return True
    except Browsing_history.DoesNotExist:
        print('Не найдено')
        return False


def browsing_history(user_id, product_id):
    """Добавление продукта в список просмотренных"""
    print('Добавляем в список')
    try:
        history = Browsing_history.objects.get(users_id=user_id,
                                               product_id=product_id)
        history.delete()
        Browsing_history.objects.create(users_id=user_id,
                                        product_id=product_id)
        print('Добавили')
    except Browsing_history.DoesNotExist:
        print('Не добавили')
        Browsing_history.objects.create(users_id=user_id,
                                        product_id=product_id)
