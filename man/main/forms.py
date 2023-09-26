from django.forms import Form, Textarea, TextInput, CharField, FileField, ChoiceField, RadioSelect


class MainForm(Form):
    text = CharField(label='', widget=Textarea(
        attrs={'placeholder': 'Текст, який буде аналізуватись', 'rows': 10, 'id': 'textar'}), required=False)
    file = FileField(label='', required=False)


class TextForm(MainForm):
    CHOICES = [
        ('1', 'Часто вживані слова'),
        ('2', 'Рідко вживані слова'),
    ]
    rad = CharField(label='', widget=RadioSelect(choices=CHOICES))


class SearchForm(MainForm):
    name = CharField(widget=TextInput(), label='Пошуковий запит')


