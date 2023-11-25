import os
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.txt']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Непідтримуваний тип файлу. Оберіть \'*.txt\'')


def validate_file_size(value):
    limit = 50 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Файл занадто великий. Використовуйте файли розміром менше ніж 50 Мб')
