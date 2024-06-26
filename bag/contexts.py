from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

# CONTEXT PROCESSOR, creating a dictionary that will be available to all templates
# need to add it to settings: TEMPLATES > OPTIONS > context_processors !
def bag_contents(request):
    # initializing variables
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})
# looping through the bag items
    for item_id, item_data in bag.items():
        if isinstance(item_data, int):
            # getting the product
            product = get_object_or_404(Product, pk=item_id)
            # calculating the total
            total += item_data * product.price
            product_count += item_data
            # appending the product to the bag_items list
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            # getting the product
            product = get_object_or_404(Product, pk=item_id)
            # looping through the sizes
            for size, quantity in item_data['items_by_size'].items():
                # calculating the total
                total += quantity * product.price
                product_count += quantity
                # appending the product to the bag_items list
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total
    
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context