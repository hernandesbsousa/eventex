# coding: utf-8

from django.test import TestCase
from django.db import IntegrityError
from datetime import datetime
from eventex.subscriptions.models import Subscription

class SubsctiptionTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Joaozinho da Silva',
            cpf='12345678902',
            email='mail@example.com',
            phone='12-20901223',
        )

    def test_has_created_at(self):
        'Subscription must have automatic created_at'
        self.obj.save()
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_create(self):
        'Subscription must have name, cpf, email, phone'
        self.obj.save()
        self.assertEqual(1, self.obj.pk)

class SubscriptionUniqueTest(TestCase):
    def setUp(self):
        Subscription.objects.create(
            name='Joaozinho da Silva',
            cpf='12345678901',
            email='mail@example.com',
            phone='12-20901223',
        )

    def test_is_cpf_unique(self):
        'CPF must be unique'
        subscription = Subscription(
            name='Joaozinho da Silva', 
            cpf='12345678901',
            email='mail@example.com', 
            phone='12-20901223'
        )
        self.assertRaises(IntegrityError, subscription.save)
