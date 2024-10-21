import time
import uuid
import logging
from random import randint
from celery import shared_task
from .models import Item


def mock_reserve(item_name):
    '''Mock function that calls an external reserve endpoint and returns a reservation_id.'''
    # This is where an external /reserve endpoint would be called
    time.sleep(randint(25, 35))
    # Simulate failure
    if item_name == 'fail_please':
        raise Exception('Reservation unsuccessful')
    return str(uuid.uuid4())

@shared_task
def reserve_item(item_id):
    try:
        item = Item.objects.get(id=item_id)
        reservation_id = mock_reserve(item.name)
        item.reservation_id = reservation_id
        item.save()
    except Exception as e:
        logging.error(f"Reservation failed for item {item_id}: {e}")
        item.delete()  # Delete the item from the cart