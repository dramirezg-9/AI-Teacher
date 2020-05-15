from django.shortcuts import render


def index(request):
    return render(request, 'index/index.html')


def about(request):
    return render(request, 'about/about.html')


def features(request):
    return render(request, 'features/features.html')
