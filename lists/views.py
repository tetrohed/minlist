from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from lists.models import Item

def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect(reverse('lists:home'))
    
    items = Item.objects.all()
    return render(request, 'lists/home.html', context={'items': items})