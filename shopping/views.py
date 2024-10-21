import random
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item, ShoppingCart
from .tasks import reserve_item

MAX_QUANTITY = 10

def mock_description(item_name):
    templates = [
        f"The {item_name} is a top-quality product that you'll love.",
        f"Experience the amazing features of the {item_name}.",
        f"Discover the versatility of the {item_name} for all your needs.",
        f"The {item_name} is perfect for anyone looking to enhance their experience.",
        f"Don't miss out on the incredible benefits of the {item_name}!"
    ]
    return random.choice(templates)

def get_session_id(request):
    session_id = request.session.session_key or request.session.create()
    return JsonResponse({'session_id': session_id})

def get_or_create_cart(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()  # Create a session if needed
        session_id = request.session.session_key

    cart, created = ShoppingCart.objects.get_or_create(id=session_id)
    return cart

@csrf_exempt
def items_endpoint(request):
    if request.method == 'GET':
        cart = get_or_create_cart(request)
        items = cart.items.all().values('name', 'description', 'reservation_id')
        return JsonResponse(list(items), safe=False)
    
    elif request.method == 'POST':
        try:
            item_data = json.loads(request.body)
            name = item_data.get('name')
            quantity = int(item_data.get('quantity', 1)) # Default is to reserve exactly one item
            if quantity > MAX_QUANTITY:
                return JsonResponse({'error': f'Cannot add more than {MAX_QUANTITY} items.'}, status=400)
            
            cart = get_or_create_cart(request)
            
            for _ in range(quantity):
                item = Item.objects.create(
                    shopping_cart=cart,
                    name=name,
                    description=mock_description(name),
                )
                reserve_item.delay(item.id)

            return JsonResponse({'message': f'{quantity} items added to cart', 'item': {'name': name}}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
