import os
import stripe
from django.conf import settings
from django.views.decorators.http import require_POST
from django.shortcuts import render


def donate(request):
    success = False

    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY

        metadata = {
            'source': request.POST.get('source', ''),
            'donor_name': request.POST.get('donor_name', ''),
        }

        customer = stripe.Customer.create(
            source=request.POST['stripeToken'],
            email=request.POST['email'],
        )
        if 'plan' in request.POST:
            subscription = stripe.Subscription.create(
                customer=customer,
                plan=request.POST['plan'],
                metadata=metadata,
            )
        else:
            # just create a one-time charge
            charge = stripe.Charge.create(
                customer=customer,
                amount=request.POST['amount'],
                currency="usd",
                description="Open States Donation",
                metadata=metadata,
            )
        success = True

    return render(request, 'flat/donate.html', {'success': success})
