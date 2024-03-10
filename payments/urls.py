from django.urls import path
from payments.views import CreateCheckoutSessionView,stripe_webhook,CancelSubscription
urlpatterns = [
    path('cancel-subscription', CancelSubscription.as_view(), name='cancel-subscription'),
    path('create-checkout-session', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook'),
]