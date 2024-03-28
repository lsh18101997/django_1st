from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def main(request):
    return HttpResponse("Hello, users. You're at the main page.")

def menu(request):
    return HttpResponse("Hello, users. You're at the menu page.")

def order(request):
    return HttpResponse("Hello, users. You're at the order page.")
