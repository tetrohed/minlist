from django.test import TestCase
from django.urls import resolve, reverse
from lists.views import home_page
from lists.models import Item
from django.http import HttpRequest
from django.template.loader import render_to_string
import unittest

class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve(reverse('lists:home'))
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get(reverse('lists:home'))
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post(reverse('lists:home'), data={'item_text': 'A new list item'})
        self.assertTemplateUsed(response, 'lists/home.html')
        self.assertIn('A new list item', response.content.decode())

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) item in list'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item in list'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) item in list')
        self.assertEqual(second_saved_item.text, 'The second item in list')
