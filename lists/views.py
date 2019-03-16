from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse

def home_page(request):
  return render(request, 'lists/home.html',
      {'new_item_text': request.POST.get('item_text', '')})