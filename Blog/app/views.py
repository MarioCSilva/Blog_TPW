from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, "layout.html")


def main_page(request):
    return render(request, "main_page.html")


def entry_page(request):
    return render(request,"entry_page.html")