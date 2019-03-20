from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from lists.models import Item

def home_page(request):    
    return render(request, 'lists/home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html', context={'items': items})

def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect(reverse('lists:view_list'))