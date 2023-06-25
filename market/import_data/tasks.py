from __future__ import absolute_import, unicode_literals
from django.utils import timezone
from django.conf import settings
from config.celery import app
import json
import os
from products.models import Import, Product
from django.core.mail import send_mail
from catalog.models import Catalog


@app.task
def import_products(file_path, email):
    try:
        with open(file_path) as f:
            data = json.load(f)
    except Exception as e:
        return 'Завершён с ошибкой', [str(e)]
    if app.control.inspect().active():
        return 'Завершён с ошибкой', ['Предыдущий импорт ещё не выполнен. Пожалуйста, дождитесь его окончания']

    log_file_name = os.path.basename(file_path) + '.log'
    log_file_path = os.path.join(settings.IMPORT_LOGS, log_file_name)

    with open(log_file_path, 'w') as log_file:
        errors = []
        products = []  # создаем пустой список для товаров
        for item in data:
            name = item.get('name')
            description = item.get('description')
            limited_edition = item.get('limited_edition')
            preview = item.get('preview')
            category = item.get('category')
            product, created = Product.objects.get_or_create(name=name, defaults={
                'name': name, 'description': description, 'limited_edition': limited_edition})
            if not created:
                product.name = name
                product.description = description
                product.limited_edition = limited_edition
                product.preview = preview
                product.save()
            category, _ = Catalog.objects.get_or_create(name=category)
            product.category = category
            product.save()
            products.append(product)
            log_file.write(f'Товар {name} был {"создан" if created else "обновлен"}\n')

        if errors:
            os.rename(file_path, os.path.join(settings.IMPORT_FAIL, os.path.basename(file_path)))
        else:
            os.rename(file_path, os.path.join(settings.IMPORT_DONE, os.path.basename(file_path)))

    subject = 'Результат импорта товаров'
    message = f'Импорт товаров из файла {file_path} был {"успешно" if not errors else "неуспешно"} выполнен.\n'
    if errors:
        message += 'В ходе импорта возникли следующие ошибки:\n'
        for error in errors:
            message += f'- {error}\n'
    message += f'Подробности импорта можно посмотреть в файле {log_file_path}.\n'
    message += 'Спасибо за использование нашего сервиса.'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    import_obj = Import.objects.get(source=file_path)
    import_obj.status = 'running'
    import_obj.start_time = timezone.now()
    import_obj.save()
    try:
        import_obj.status = 'completed'
        import_obj.end_time = timezone.now()
        import_obj.imported_count = len(products)
        import_obj.save()
        return f'Импорт из {file_path} успешно завершен. Импортировано {len(products)} товаров.'
    except Exception as e:
        import_obj.status = 'failed'
        import_obj.end_time = timezone.now()
        import_obj.errors.append(str(e))
        import_obj.save()
        return f'Импорт из {file_path} завершен с ошибкой. Ошибка: {e}'
