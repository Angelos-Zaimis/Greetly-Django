import json
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import HttpResponse, JsonResponse
import stripe
from django.views.decorators.csrf import csrf_exempt
from custom_user.models import User

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
class CreateCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        body_data = json.loads(request.body.decode('utf-8'))
        if 'priceId' in body_data:
            priceId = body_data['priceId']
        if 'user_email' in body_data:
            user_email = body_data['user_email']

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': priceId,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            metadata={
                'user_email': user_email
            },
            success_url='http://localhost:3000/payments/success',
            cancel_url='http://localhost:3000/payments/cancel'
        )

        data = {
            'checkout': checkout_session.url
        }

        return HttpResponse(json.dumps(data), content_type='application/json', status=200)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        customer_email = session['customer_details']['email']
        if session.payment_status == "paid":
            send_mail(
                subject="Monthly subscription",
                message="Thank you very much for your purchase.You monthly subscription is now active.",
                recipient_list=[customer_email],
                from_email="www.greetly.ch"
            )
            user_email = session['metadata']['user_email']
            user = User.objects.get(email=user_email)

            user.isSubscribed = True
            user.product_details['subscription_price'] = session['amount_total']
            user.product_details['subscription_plan'] = session['line_items']['data'][0]['price']['recurring'][
                'interval']
            user.product_details['subscription_currency'] = session['line_items']['data'][0]['currency']
            user.product_details['subscription_id'] = session['subscription']

            user.save()

        elif event['type'] == 'checkout.session.async_payment_failed':
            session = event['data']['object']

    return HttpResponse(status=200)


class CancelSubscription(View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        user_email = data.get('email')

        subscription_id = data.get('subscription_id')

        response = stripe.Subscription.delete(
            subscription_id,
        )

        if response.cancellation_details:
            # Subscription was successfully canceled
            user = User.objects.get(email=user_email)

            # Update user details
            user.isSubscribed = False
            user.product_details['subscription_price'] = ""
            user.product_details['subscription_plan'] = ""
            user.product_details['subscription_currency'] = ""
            user.product_details['subscription_id'] = ""

            user.save()

            # Return a success response
            return JsonResponse({'message': 'Subscription successfully canceled'}, status=200)
        else:
            # Subscription could not be canceled, inform the user
            return JsonResponse({'error': 'Failed to cancel subscription'}, status=400)
