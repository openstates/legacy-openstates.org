from django.conf import settings


def stripe_settings(request):
    return {
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        'STRIPE_PLANS': settings.STRIPE_PLANS,
    }
