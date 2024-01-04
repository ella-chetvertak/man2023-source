from django.forms import Form, Textarea, TextInput, CharField, FileField, RadioSelect, BooleanField, CheckboxInput
from .validators import validate_file_extension, validate_file_size


class MainForm(Form):
    text = CharField(label='', widget=Textarea(
        attrs={'placeholder': 'Текст, який буде аналізуватись', 'rows': 10, 'id': 'textar'}), required=False)
    file = FileField(label='', validators=[validate_file_extension, validate_file_size], required=False)
    file.widget.attrs['id'] = 'filear'


class TextForm(MainForm):
    CHOICES = [
        ('1', 'Часто вживані слова'),
        ('2', 'Рідко вживані слова'),
    ]
    rad = CharField(label='', widget=RadioSelect(choices=CHOICES))


class SearchForm(MainForm):
    name = CharField(widget=TextInput(), label='Пошуковий запит')
    check_case = BooleanField(label="Враховувати регістр", required=False)


class NLTKForm(MainForm):
    min_ton = CharField(widget=TextInput(attrs={'class': 'minmax-input'}), label='Мінімальний настрій (у процентах від -100 до 100) (за зам. -100%)', required=False)
    max_ton = CharField(widget=TextInput(attrs={'class': 'minmax-input'}), label='Максимальний настрій (за зам. 100%)', required=False)


class SettingsForm(Form):
    group_size = CharField(widget=TextInput(attrs={'class': 'minmax-input', 'type': 'number'}), label='Розмір групи слів (5 за замовчуванням, ЧВС)', required=False)
    freq = CharField(widget=TextInput(attrs={'class': 'minmax-input', 'type': 'number'}), label='Частота рідкісних слів (1 за замовчуванням)', required=False)
