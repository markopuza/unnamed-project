from django.test import TestCase
from django.urls import reverse
from unittest import mock
from shopping.models import Item, ShoppingCart, RESERVATION_IN_PROGRESS
from shopping.views import MAX_QUANTITY

class ShoppingCartTests(TestCase):
    def setUp(self):
        self.url = reverse('items')

    @mock.patch('shopping.tasks.mock_reserve', return_value="reservation-123")
    def test_add_items_to_cart_success(self, mock_reserve):
        data = {
            'name': 'test-item',
            'quantity': 2
        }
        response = self.client.post(self.url, data, content_type='application/json', HTTP_COOKIE='sessionid=test-session-id')

        # Check items were created with the reservation pending placeholder
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Item.objects.count(), 2)
        item = Item.objects.first()
        self.assertEqual(item.name, 'test-item')
        self.assertEqual(item.reservation_id, RESERVATION_IN_PROGRESS)

        # Check the shopping cart was created with the right session_id
        self.assertEqual(ShoppingCart.objects.count(), 1)
        cart = ShoppingCart.objects.first()
        self.assertEqual(cart.id, 'test-session-id')

        # Check the items are linked to the appropriate cart
        self.assertEqual(item.shopping_cart, cart)

    def test_add_item_to_cart_too_many(self):
        data = {
            'name': 'test-item',
            'quantity': MAX_QUANTITY + 1
        }
        response = self.client.post(self.url, data, content_type='application/json', HTTP_COOKIE='sessionid=test-session-id')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], f'Cannot add more than {MAX_QUANTITY} items.')
        self.assertEqual(Item.objects.count(), 0)