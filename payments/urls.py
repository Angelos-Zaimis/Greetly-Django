from django.urls import path
from payments.views import CreateCheckoutSessionView,stripe_webhook,CancelSubscription
urlpatterns = [
    path('create-checkout-session', CreateCheckoutSessionView.as_view(), name='creat-checkout-session'),
    path('webhooks/stripe-webhook', stripe_webhook, name='stripe-webhook'),
    path('cancel-subscription', CancelSubscription.as_view(), name='cancel-subscription')
]