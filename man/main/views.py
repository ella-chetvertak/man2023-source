from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from .forms import TextForm, SearchForm, NLTKForm, SettingsForm
from nltk.tokenize import sent_tokenize
from .text_an import TextAnalyser
from .nltk_an import NLTKAnalyse
import re
from json import dumps


def index(request):
    response = render(request, 'main/index.html')
    check = request.COOKIES.get('check')
    if check != '1':
        response.set_cookie('group_size', 5)
        response.set_cookie('freq', 1)
        response.set_cookie('check', 1)
    return response


def summarise(request, clean_text, group_size, freq):
    text_analyse = None
    if request.FILES:
        text_analyse = TextAnalyser(request.FILES['file'], True, group_size, freq)
    elif clean_text:
        text_analyse = TextAnalyser(clean_text, False, group_size, freq)
    return text_analyse


def often(request):
    if request.method == 'POST':
        if request.FILES:
            form = TextForm(request.POST, request.FILES)
        else:
            form = TextForm(request.POST)
        if form.is_valid():
            clean_text = form.cleaned_data['text']
            clean_data = form.cleaned_data
            group_size = int(request.COOKIES.get('group_size'))
            freq = int(request.COOKIES.get('freq'))
            text_analyse = summarise(request, clean_text, group_size, freq)
            if not text_analyse:
                data = {
                    'form': form,
                    'info': 'Введіть текст або оберіть файл',
                }
                return render(request, 'main/often.html', data)

            text_analyse.at_start()

            if clean_data['rad'] == '1':
                text_analyse.analyse_popular()
                clean_text = mark_safe(text_analyse.resultsPop)
            elif clean_data['rad'] == '2':
                text_analyse.analyse_rare()
                clean_text = text_analyse.resultsRare

            data = {
                'form': form,
                'info': clean_text,
            }
        else:
            data = {
                'form': TextForm(),
                'info': form.errors,
            }
        return render(request, 'main/often.html', data)
    else:
        form = TextForm(initial={'rad': '1'})

    return render(request, 'main/often.html', {"form": form})


def search(request):
    if request.method == 'POST':
        if request.FILES:
            form = SearchForm(request.POST, request.FILES)
        else:
            form = SearchForm(request.POST)

        if form.is_valid():
            clean_text = form.cleaned_data['text']
            clean_data = form.cleaned_data
            group_size = int(request.COOKIES.get('group_size'))
            freq = int(request.COOKIES.get('freq'))
            text_analyse = summarise(request, clean_text, group_size, freq)
            if not text_analyse:
                data = {
                    'form': form,
                    'info': 'Введіть текст або оберіть файл',
                }
                return render(request, 'main/search.html', data)

            text_analyse.at_start()

            name = clean_data['name']
            text_analyse.search_ctx(name)
            clean_text = text_analyse.resCtx
            all_entries = set(re.findall(fr'(?i){name}', clean_text))
            for elem in all_entries:
                clean_text = re.sub(elem, f'<mark>{elem}</mark>', clean_text)
            clean_text = mark_safe(clean_text)

            data = {
                'form': form,
                'info': clean_text,
            }
        else:
            data = {
                'form': SearchForm(),
                'info': form.errors,
            }
        return render(request, 'main/search.html', data)
    else:
        form = SearchForm()

    return render(request, 'main/search.html', {"form": form})


def summarise_nltk(request, clean_text, min_ton, max_ton):
    nltk_analyse = None
    if request.FILES:
        nltk_analyse = NLTKAnalyse(request.FILES['file'], True, min_ton, max_ton)
    elif clean_text:
        nltk_analyse = NLTKAnalyse(clean_text, False, min_ton, max_ton)
    return nltk_analyse


def nltk_ton(request):
    if request.method == 'POST':
        if request.FILES:
            form = NLTKForm(request.POST, request.FILES)
        else:
            form = NLTKForm(request.POST)
        if form.is_valid():
            clean_text = form.cleaned_data['text']
            clean_data = form.cleaned_data

            min_ton = clean_data['min_ton']
            max_ton = clean_data['max_ton']

            if clean_data['min_ton'] == '':
                min_ton = -100
            if clean_data['max_ton'] == '':
                max_ton = 100

            nltk_analyse = summarise_nltk(request, clean_text, min_ton, max_ton)
            if not nltk_analyse:
                data = {
                    'form': form,
                    'info': 'Введіть текст або оберіть файл',
                }
                return render(request, 'main/nltk_ton.html', data)

            nltk_analyse.at_start()

            totalX, totalY = nltk_analyse.get_every_analyse()

            clean_text = "Загальна тональність тексту (без урахування обмежень): " + "%.2f" % nltk_analyse.aver_percent + ' %' + '<br><br>'
            clean_text += 'Діаграму створено'
            clean_text = mark_safe(clean_text)
            chart_data = {'totalX': totalX, 'totalY': totalY}
            chart_data_json = dumps(chart_data)

            data = {
                'form': form,
                'info': clean_text,
                'data': chart_data_json,
            }
        else:
            data = {
                'form': NLTKForm(),
                'info': form.errors,
                'data': dumps({'totalX': [], 'totalY': []}),
            }
        return render(request, 'main/nltk_ton.html', data)
    else:
        form = NLTKForm()

    return render(request, 'main/nltk_ton.html', {"form": form})


def reset_settings(request):
    form = SettingsForm()
    data = {
        'form': form,
        'info': 'Дані зкинуто до початкових налаштувань'
    }
    response = render(request, 'main/settings.html', data)
    response.set_cookie('group_size', 5)
    response.set_cookie('freq', 1)
    return response


def settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            if clean_data['group_size']:
                group_size = int(clean_data['group_size'])
            if clean_data['freq']:
                freq = int(clean_data['freq'])
            data = {
                'form': form,
                'info': 'Дані збережені',
            }
        else:
            group_size = 5
            freq = 1
            data = {
                'form': SettingsForm(),
                'info': form.errors,
            }
        response = render(request, 'main/settings.html', data)
        if clean_data['group_size']:
            response.set_cookie("group_size", group_size)
        if clean_data['freq']:
            response.set_cookie("freq", freq)
        return response
    elif request.method == 'UPDATE':
        form = SettingsForm()
        data = {
            'form': form,
            'info': 'Дані зкинуто до початкових налаштувань',
        }
        response = render(request, 'main/settings.html', data)
        response.set_cookie('group_size', 5)
        response.set_cookie('freq', 1)
        return response
    else:
        form = SettingsForm()
    return render(request, 'main/settings.html', {"form": form})
