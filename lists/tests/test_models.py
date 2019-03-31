import unittest

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve, reverse
from django.core.exceptions import ValidationError

from lists.models import Item, List
from lists.views import home_page


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        new_list = List()
        new_list.save()

        first_item = Item()
        first_item.text = 'The first (ever) item in list'
        first_item.list = new_list
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item in list'
        second_item.list = new_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, new_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text,
                         'The first (ever) item in list')
        self.assertEqual(second_saved_item.text, 'The second item in list')

        self.assertEqual(first_saved_item.list, new_list)
        self.assertEqual(second_saved_item.list, new_list)

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError): 
            item.save() 
            item.full_clean()

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')
