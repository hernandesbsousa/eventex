# coding: utf-8

from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription

class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        'GET /inscricao should return status code 200'
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        'Response should be a rendered template from subscription form'
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        'Html should contain all input controls'
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        'Html must contain csrf token.'
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        'Content must have the subscription form'
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Joaozinho da Silva',
                    cpf='12345678901',
                    email='joao@example.com',
                    phone='11-3878-1111'
                )
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        'Valid POST should redirect to /inscricao/1/'
        self.assertEqual(302, self.resp.status_code)

    def test_save(self):
        'Valid POST must be saved'
        self.assertTrue(Subscription.objects.exists())

class SubscribeInvalidPostTest(TestCase):
    def setUp(self):
        data = dict(name='Joaozinho da Silva',
                    cpf='123456789012',
                    email='joao@example.com',
                    phone='11-3878-1111'
                )
        self.resp = self.client.post('/inscricao/', data)

    def test_invalid_post(self):
        'Invalid POST should not redirect.'
        self.assertEqual(200, self.resp.status_code)

    def test_form_errors(self):
        'Form must contain errors.'
        self.assertTrue(self.resp.context['form'].errors)

    def test_dont_save(self):
        'Invalid post should not save data'
        self.assertFalse(Subscription.objects.exists())