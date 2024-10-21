from django.test import TestCase
from unittest import mock
from shopping.models import Item
from shopping.tasks import reserve_item

class ShoppingCartTaskTests(TestCase):
    def setUp(self):
        self.item = Item.objects.create(name="test-item", description="Test item")

    @mock.patch('shopping.tasks.mock_reserve', side_effect=Exception("Reservation failed"))
    def test_reservation_failure_deletes_item(self, mock_reserve):
        reserve_item(self.item.id)
        self.assertEqual(Item.objects.count(), 0)
        mock_reserve.assert_called_once()

    @mock.patch('shopping.tasks.mock_reserve', return_value="reservation-123")
    def test_reservation_success_updates_item(self, mock_reserve):
        reserve_item(self.item.id)
        self.item.refresh_from_db()
        self.assertEqual(self.item.reservation_id, "reservation-123")
        mock_reserve.assert_called_once()