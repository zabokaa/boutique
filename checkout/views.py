from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm
from bag.contexts import bag_contents


def checkout(request):
    """
    A view to return the checkout page
    """
    # get bag from session + check if it's empty
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))
# create instance for order form
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51PIvxGATjyvbumTol8JLREvXxbVqfydItJDu7lGDAzsmlxG9an1kOuuKOCw30wTsTTjLarwb2iFLpgS0TliXv7fJ00RKcaEdtD',
        'client_secret': 'test client secret',
    }
# rendering it all out
    return render(request, template, context)
