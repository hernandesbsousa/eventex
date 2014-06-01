# coding: utf-8

from django.test import TestCase
from eventex.subscriptions.models import Subscription

class DetailTest(TestCase):
    def setUp(self):
        subscription = Subscription.objects.create(
            name='Joaozinho',
            cpf='123',
            email='mail@example.com',
            phone='123',
            )
        self.resp = self.client.get('/inscricao/%d/' % subscription.pk)

    def test_get(self):
        'GET /inscricao/1 should return status code 200.'
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        'Uses template.'
        self.assertTemplateUsed(self.resp,
                                    'subscriptions/subscription_detail.html')

    def test_context(self):
        'Context must have a subscription instance.'
        subscription = self.resp.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        'Check if subscription data was rendered'
        self.assertContains(self.resp, 'Joaozinho')

class DetailNotFound(TestCase):
    def test_not_found(self):
        response = self.client.get('/inscricao/0/')
        self.assertEqual(404, response.status_code)