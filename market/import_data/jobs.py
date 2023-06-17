import os
import shutil
import requests
import json
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django_rq import job  # для создания фоновой задачи
from catalog.models import Catalog
from products.models import Product


class ImportJob:
    def __init__(self, source, email, save):
        """инициализация атрибутов класса"""
        self.source = source  # имя файла или URL для импорта
        self.email = email  # email получателя уведомления
        self.save = save  # флаг для сохранения данных в базу
        self.data = None  # данные для импорта в виде списка словарей
        self.status = None  # статус выполнения импорта
        self.errors = []  # список ошибок при импорте
        self.log_file = None  # файл для записи лога работы

    def run(self):
        """запускает фоновую задачу с помощью декоратора @job"""
        @job
        def import_data():
            """проверяет, есть ли другой процесс импорта"""
            if self.is_another_import_running():
                # если есть, то возвращаем ошибку и прерываем импорт
                self.status = 'Завершен с ошибкой'
                self.errors.append('Предыдущий импорт еще не выполнен. Пожалуйста, дождитесь его окончания')
                return

            # если нет, то начинаем импорт
            self.status = 'В процессе выполнения'

            # создаем файл для записи лога работы и открываем его для записи
            self.log_file = open(f'logs/import_{self.source}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt', 'w')

            # читаем и парсим файл или URL для импорта
            self.read_and_parse_source()

            # преобразуем данные в формат, подходящий для моделей django
            self.transform_data()

            # если указан флаг для сохранения данных в базу, то сохраняем их
            if self.save:
                self.save_data()

            # перемещаем файл в соответствующую папку в зависимости от статуса импорта
            self.move_file()

            # закрываем файл лога
            self.log_file.close()

            # отправляем уведомление по email, если указан получатель
            if self.email:
                self.send_notification()

        # вызываем фоновую задачу без аргументов
        import_data.delay()

    def is_another_import_running(self):
        """проверяет, есть ли другой процесс импорта по наличию файла с расширением .lock в папке import_data"""
        return any(file.endswith('.lock') for file in os.listdir('import_data'))

    def read_and_parse_source(self):
        """читает и парсит файл или URL для импорта"""

        try:
            # если источник - это URL, то делаем запрос с помощью requests и получаем содержимое ответа в виде строки
            if self.source.startswith('http'):
                response = requests.get(self.source)
                content = response.text

            # если источник - это файл, то открываем его и читаем содержимое в виде строки
            else:
                with open(os.path.join('import_data', self.source), 'r') as file:
                    content = file.read()

            # загружаем содержимое в словарь с помощью json и извлекаем список элементов по ключу 'items'
            data_dict = json.loads(content)
            self.data = data_dict['items']

            # записываем в лог успешное чтение и парсинг файла или URL
            self.log_file.write(f'Прочитан и распарсен файл или URL {self.source}\n')

        except Exception as e:
            # если возникла ошибка, то записываем ее в лог и добавляем в список ошибок
            self.log_file.write(f'Ошибка при чтении или парсинге файла или URL {self.source}: {e}\n')
            self.errors.append(f'Ошибка при чтении или парсинге файла или URL {self.source}: {e}')

    def transform_data(self):
        """преобразует данные в формат, подходящий для моделей django"""

        try:
            # создаем пустой список для хранения преобразованных данных
            transformed_data = []

            # проходим по каждому элементу в списке данных
            for item in self.data:
                # извлекаем значения полей из словаря
                name = item['name']
                description = item['description']
                limited_edition = item['limited_edition']
                category = item['category']
                preview = item['preview']

                # создаем словарь с ключами, соответствующими полям модели Product
                product_data = {
                    'name': name,
                    'description': description,
                    'limited_edition': limited_edition,
                    'category': category,
                    'preview': preview,
                }

                # добавляем словарь в список преобразованных данных
                transformed_data.append(product_data)

            # перезаписываем атрибут data списком преобразованных данных
            self.data = transformed_data

            # записываем в лог успешное преобразование данных
            self.log_file.write(f'Преобразованы данные из файла или URL {self.source}\n')

        except Exception as e:
            # если возникла ошибка, то записываем ее в лог и добавляем в список ошибок
            self.log_file.write(f'Ошибка при преобразовании данных из файла или URL {self.source}: {e}\n')
            self.errors.append(f'Ошибка при преобразовании данных из файла или URL {self.source}: {e}')

    def save_data(self):
        """сохраняет данные в базу данных"""

        try:
            # проходим по каждому элементу в списке данных
            for item in self.data:
                # извлекаем значения полей из словаря
                name = item['name']
                description = item['description']
                limited_edition = item['limited_edition']
                category = item['category']
                preview = item['preview']

                # получаем или создаем объекты моделей Category, Manufacturer и Seller по именам
                category_obj, _ = Catalog.objects.get_or_create(name=category)

                # создаем объект модели Product с указанными значениями полей и связями с другими моделями
                product_obj = Product.objects.create(
                    name=name,
                    description=description,
                    limited_edition=limited_edition,
                    category=category_obj,
                    preview=preview,
                )

                # записываем в лог успешное сохранение товара в базу данных
                self.log_file.write(f'Сохранен товар {name} в базу данных\n')

            # записываем в лог успешное сохранение всех данных в базу данных
            self.log_file.write(f'Сохранены все данные из файла или URL {self.source} в базу данных\n')

        except Exception as e:
            # если возникла ошибка, то записываем ее в лог и добавляем в список ошибок
            self.log_file.write(f'Ошибка при сохранении данных из файла или URL {self.source} в базу данных: {e}\n')
            self.errors.append(f'Ошибка при сохранении данных из файла или URL {self.source} в базу данных: {e}')

    def move_file(self):
        """перемещает файл в соответствующую папку в зависимости от статуса импорта"""

        try:
            # если источник - это файл, а не URL, то перемещаем его
            if not self.source.startswith('http'):
                # определяем путь к файлу в папке import_data
                source_path = os.path.join('import_data', self.source)

                # если в списке ошибок нет элементов, то считаем, что импорт был успешным
                if not self.errors:
                    # определяем путь к папке success в папке imported_data
                    destination_path = os.path.join('imported_data', 'success')

                    # устанавливаем статус импорта как "Выполнен"
                    self.status = 'Выполнен'

                # если в списке ошибок есть элементы, то считаем, что импорт был неуспешным
                else:
                    # определяем путь к папке failure в папке imported_data
                    destination_path = os.path.join('imported_data', 'failure')

                    # устанавливаем статус импорта как "Завершен с ошибкой"
                    self.status = 'Завершен с ошибкой'

                # перемещаем файл из исходной папки в целевую папку
                shutil.move(source_path, destination_path)

                # записываем в лог успешное перемещение файла
                self.log_file.write(f'Перемещен файл {self.source} из папки import_data в папку {destination_path}\n')

            # если источник - это URL, то ничего не делаем
            else:
                # записываем в лог, что перемещение файла не требуется
                self.log_file.write(f'Перемещение файла не требуется, так как источник - это URL {self.source}\n')

        except Exception as e:
            # если возникла ошибка, то записываем ее в лог и добавляем в список ошибок
            self.log_file.write(f'Ошибка при перемещении файла {self.source}: {e}\n')
            self.errors.append(f'Ошибка при перемещении файла {self.source}: {e}')

    def send_notification(self):
        """отправляет уведомление по email, если указан получатель"""

        try:
            # формируем тему и текст сообщения на основе статуса и ошибок импорта
            subject = f'Результат импорта из файла или URL {self.source}'
            message = f'Импорт из файла или URL {self.source} был {self.status.lower()}.\n'
            if self.errors:
                message += f'В процессе импорта возникли следующие ошибки:\n'
                for error in self.errors:
                    message += f'- {error}\n'

            # отправляем сообщение по указанному email с помощью django.core.mail.send_mail
            send_mail(subject, message, settings.EMAIL_HOST_USER, [self.email])

            # записываем в лог успешную отправку уведомления
            self.log_file.write(f'Отправлено уведомление по email {self.email} о результате импорта\n')

        except Exception as e:
            # если возникла ошибка, то записываем ее в лог и добавляем в список ошибок
            self.log_file.write(f'Ошибка при отправке уведомления по email {self.email}: {e}\n')
            self.errors.append(f'Ошибка при отправке уведомления по email {self.email}: {e}')
