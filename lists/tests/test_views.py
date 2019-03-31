import unittest

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils.html import escape

from lists.models import Item, List
from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve(reverse('lists:home'))
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get(reverse('lists:home'))
        self.assertTemplateUsed(response, 'lists/home.html')


class NewListTests(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post(reverse('lists:new_list'), data={
                         'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post(reverse('lists:new_list'), data={
                                    'item_text': 'A new list item'})
        self.assertRedirects(response, reverse(
            'lists:view_list', kwargs={'list_id': 1}))

    def test_validation_errors_are_sent_bakc_to_home_page_template(self):
        response = self.client.post(reverse('lists:new_list'), data={
                                    'item_text': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')
        expected_error = "You can't have an empty list item"
        self.assertContains(response, escape(expected_error))

    def test_invalid_items_are_not_saved(self):
        response = self.client.post(reverse('lists:new_list'), data={
                                    'item_text': ''})

        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class ListViewTests(TestCase):

    def test_displays_items_only_for_the_corresponding_list(self):
        list_ = List.objects.create()
        Item.objects.create(text='item 1', list=list_)
        Item.objects.create(text='item 2', list=list_)

        otherList = List.objects.create()
        Item.objects.create(text='other item 1', list=otherList)
        Item.objects.create(text='other item 2', list=otherList)

        response = self.client.get(
            reverse('lists:view_list', kwargs={'list_id': list_.id}))

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'other item 1')
        self.assertNotContains(response, 'other item 2')

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(
            reverse('lists:view_list', kwargs={'list_id': list_.id}))
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_passes_correct_list_to_template_context(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(
            reverse('lists:view_list', kwargs={'list_id': correct_list.id}))

        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(reverse('lists:view_list', kwargs={'list_id': correct_list.id}),
                         data={'item_text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        list_ = List.objects.create()

        response = self.client.post(reverse('lists:view_list', kwargs={'list_id': list_.id}),
                                    data={'item_text': 'A new item for list'})

        self.assertRedirects(response, reverse(
            'lists:view_list', kwargs={'list_id': 1}))
