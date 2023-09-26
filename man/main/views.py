from django.shortcuts import render
from django.utils.safestring import mark_safe
from .forms import TextForm, SearchForm, MainForm
from nltk.tokenize import sent_tokenize
import random
import codecs
from pathlib import Path
import os

from .text_an import TextAnalyser
from .nltk_an import NLTKAnalyse


def index(request):
    return render(request, 'main/index.html')


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

            if request.FILES:
                text_analyse = TextAnalyser(request.FILES['file'], True)
            else:
                text_analyse = TextAnalyser(clean_text, False)

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
                'form': 'Not valid'
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

            if request.FILES:
                text_analyse = TextAnalyser(request.FILES['file'], True)
            else:
                text_analyse = TextAnalyser(clean_text, False)

            text_analyse.at_start()

            text_analyse.search_ctx(clean_data['name'])
            clean_text = mark_safe(text_analyse.resCtx)

            data = {
                'form': form,
                'info': clean_text,
            }
        else:
            data = {
                'form': 'Not valid'
            }
        return render(request, 'main/search.html', data)
    else:
        form = SearchForm()

    return render(request, 'main/search.html', {"form": form})


def nltk_ton(request):
    if request.method == 'POST':
        if request.FILES:
            form = MainForm(request.POST, request.FILES)
        else:
            form = MainForm(request.POST)
        print(form.errors)
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

            sentencesOut = sent_tokenize(clean_text)
            nltk_analyse = NLTKAnalyse(sentencesOut)

            clean_text = nltk_analyse.get_every_analyse() + '<br><br>'
            clean_text += "%.2f" % nltk_analyse.aver_percent + ' %'
            clean_text = mark_safe(clean_text)

            data = {
                'form': form,
                'info': clean_text,
            }
        else:
            data = {
                'form': 'Not valid'
            }
        return render(request, 'main/nltk_ton.html', data)
    else:
        form = MainForm()

    return render(request, 'main/nltk_ton.html', {"form": form})
