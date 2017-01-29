import os
import stripe
from django.views.decorators.http import require_POST


@require_POST
def donate(request):
    stripe.api_key = os.environ['STRIPE_API_KEY']

    customer = stripe.Customer.create(
        source=request.POST['stripeToken'],
        email=request.POST['email'],
    )
    if 'plan' in request.POST:
        subscription = stripe.Subscription.create(
            customer=customer,
            plan=request.POST['plan'],
        )
    else:
        # just create a one-time charge
        charge = stripe.Charge.create(
            customer=customer,
            amount=request.POST['amount'],
            currency="usd",
            description="Open States Donation",
        )
