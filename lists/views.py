from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from lists.models import Item

def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect(reverse('lists:home') + 'the-only-list-in-the-world/')
    
    return render(request, 'lists/home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html', context={'items': items})
