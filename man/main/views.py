from django.shortcuts import render
from django.utils.safestring import mark_safe
from .forms import TextForm, SearchForm, NLTKForm, SettingsForm
from nltk.tokenize import sent_tokenize
import codecs
from .text_an import TextAnalyser
from .nltk_an import NLTKAnalyse
import re


def index(request):
    response = render(request, 'main/index.html')
    check = request.COOKIES.get('check')
    if check != '1':
        response.set_cookie('group_size', 5)
        response.set_cookie('freq', 1)
        response.set_cookie('check', 1)
    return response


def often(request):
    if request.method == 'POST':
        if request.FILES:
            form = TextForm(request.POST, request.FILES)
        else:
            form = TextForm(request.POST)
        print(form.errors)
        if form.is_valid():
            clean_text = form.cleaned_data['text']
            clean_data = form.cleaned_data
            group_size = int(request.COOKIES.get('group_size'))
            freq = int(request.COOKIES.get('freq'))
            if request.FILES:
                text_analyse = TextAnalyser(request.FILES['file'], True, group_size, freq)
            else:
                text_analyse = TextAnalyser(clean_text, False, group_size, freq)

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
            if request.FILES:
                text_analyse = TextAnalyser(request.FILES['file'], True, group_size, freq)
            else:
                text_analyse = TextAnalyser(clean_text, False, group_size, freq)

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


def nltk_ton(request):
    if request.method == 'POST':
        if request.FILES:
            form = NLTKForm(request.POST, request.FILES)
        else:
            form = NLTKForm(request.POST)
        if form.is_valid():
            clean_text = form.cleaned_data['text']
            clean_data = form.cleaned_data

            if request.FILES:
                with open("textForm.txt", "wb+") as destination:
                    for chunk in request.FILES['file'].chunks():
                        destination.write(chunk)
                file = codecs.open('textForm.txt', "r", "utf-8")
                clean_text = file.read()
                file.close()
            elif not clean_text:
                file = codecs.open('textForm.txt', "r", "utf-8")
                clean_text = file.read()
                file.close()

            sentencesOut = sent_tokenize(clean_text)

            min_ton = clean_data['min_ton']
            max_ton = clean_data['max_ton']

            if clean_data['min_ton'] == '':
                min_ton = 0
            if clean_data['max_ton'] == '':
                max_ton = 100

            nltk_analyse = NLTKAnalyse(sentencesOut, min_ton, max_ton)

            every_ton = nltk_analyse.get_every_analyse()

            clean_text = "Загальна тональність тексту (без урахування обмежень): " + "%.2f" % nltk_analyse.aver_percent + ' %' + '<br><br>'
            clean_text += every_ton
            clean_text = mark_safe(clean_text)

            data = {
                'form': form,
                'info': clean_text,
            }
        else:
            data = {
                'form': NLTKForm(),
                'info': form.errors,
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
