from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from static.python.process_request import process_request


def index(request):
    return render(request, 'index/index.html')


def solve(request):
    return render(request, 'solve/solve.html')


def features(request):
    return render(request, 'features/features.html')


def grade(request):
    history = json.loads(request.POST["history"])
    processed_history = process_request(history)
    return JsonResponse(processed_history)


def about(request):
    return render(request, 'about/about.html')
