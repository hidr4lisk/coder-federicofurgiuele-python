from django.shortcuts import render

def index(request):
    return render(request, "biblioteca/index.html")