from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from lists.models import Item, List
from django.core.exceptions import ValidationError


def home_page(request):
    return render(request, 'lists/home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    if request.method == 'POST':
        item = Item(text=request.POST['item_text'], list=list_)
        try:
            item.full_clean()
            item.save()
        except:
            return render(request, 'lists/list.html',
                          context={'list': list_,
                                   'error': "You can't have an empty list item"})

        return redirect(list_)

    return render(request, 'lists/list.html', context={'list': list_})


def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        return render(request, 'lists/home.html', context={'error': "You can't have an empty list item"})
    return redirect(list_)
