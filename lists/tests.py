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
        self.client.post(reverse('lists:home'), data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post(reverse('lists:home'), data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], reverse('lists:home') + 'the-only-list-in-the-world/')

    def test_only_save_new_item_with_POST_request(self):
        count_items_before_get = Item.objects.count()
        self.client.get(reverse('lists:home'))
        count_items_after_get = Item.objects.count()
        self.assertEqual(count_items_after_get, count_items_before_get)


class ListViewTests(TestCase):

    def test_display_all_list_items(self):
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        response = self.client.get(reverse('lists:view_list'))

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')

    def test_uses_list_template(self):
        response = self.client.get(reverse('lists:view_list'))
        self.assertTemplateUsed(response, 'lists/list.html')

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
