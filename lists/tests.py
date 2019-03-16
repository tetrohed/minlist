from django.test import TestCase
from django.urls import resolve, reverse
from lists.views import home_page
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