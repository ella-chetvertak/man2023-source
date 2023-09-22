from django.shortcuts import render
from django.utils.safestring import mark_safe
from .forms import TextForm, SearchForm
import random
from pathlib import Path
import os

from .text_an import TextAnalyser


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
