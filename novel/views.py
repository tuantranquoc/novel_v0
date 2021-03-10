from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from novel import crawler
# Create your views here.


def index(request):
    crawler.get_url_from_main_page("href")
    return HttpResponse("<h3>This is the response<h3>")
