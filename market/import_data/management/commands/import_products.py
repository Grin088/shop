from django.core.management.base import BaseCommand
from import_data.tasks import import_products

class Command(BaseCommand):
    """класс для команды импорта данных"""

    help = 'Import data from file or URL'  # справочное сообщение

    def add_arguments(self, parser):
        """метод для добавления аргументов к команде"""
        parser.add_argument('source', type=str,
                            help='File name or URL for import_files')
        parser.add_argument('--email', type=str,
                            help='Email recipient for notification')
        parser.add_argument('--save', action='store_true',
                            help='Save import_files object to database')

    def handle(self, *args, **options):
        """метод для выполнения команды"""

        # получаем значения аргументов из options
        source = options['source']
        # email = options['email']
        # save = options['save']

        # запускаем задачу импорта с помощью celery
        task = import_products.delay(source)

        # получаем идентификатор задачи
        task_id = task.id

        # выводим информацию о статусе и результате задачи
        self.stdout.write(f'Задача импорта запущена с идентификатором {task_id}')
        self.stdout.write(f'Статус задачи: {task.status()}')
        self.stdout.write(f'Результат задачи: {task.get()}')
