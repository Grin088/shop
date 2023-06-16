from django.core.management.base import BaseCommand
from ...jobs import ImportJob

class Command(BaseCommand):
    """класс для команды импорта данных"""

    help = 'Import data from file or URL'  # справочное сообщение

    def add_arguments(self, parser):
        # метод для добавления аргументов к команде
        parser.add_argument('source', type=str,
                            help='File name or URL for import_files')  # обязательный аргумент с именем файла или URL для импорта
        parser.add_argument('--email', type=str,
                            help='Email recipient for notification')  # необязательный аргумент с email получателя уведомления
        parser.add_argument('--save', action='store_true',
                            help='Save import_files object to database')  # необязательный аргумент-флаг для сохранения объекта импорта в базу данных

    def handle(self, *args, **options):
        # метод для выполнения команды

        # получаем значения аргументов из options
        source = options['source']
        email = options['email']
        save = options['save']

        # создаем экземпляр класса ImportJob с переданными аргументами
        job = ImportJob(source, email, save)

        # запускаем метод run() класса ImportJob для выполнения импорта
        job.run()
        # # выводим информационное сообщение о начале импорта
        # self.stdout.write(f'Starting import_files from {source}')
        #
        # # если указан флаг save, то создаем объект модели Import с указанным источником и email
        # if save:
        #     import_obj = Import.objects.create(source=source, email=email)
        #     # выводим информационное сообщение о создании объекта импорта
        #     self.stdout.write(f'Created import_files object with id {import_obj.id}')
        # else:
        #     # иначе присваиваем переменной import_obj значение None
        #     import_obj = None
        #
        # # получаем очередь по умолчанию из django-rq
        # queue = get_queue()
        #
        # # ставим в очередь функцию run_import с указанными аргументами
        # queue.enqueue(run_import, source, email, import_obj)
        #
        # # выводим информационное сообщение об окончании команды
        # self.stdout.write(f'Finished command for {source}')