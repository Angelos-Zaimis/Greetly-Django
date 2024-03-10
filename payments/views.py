import json
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.permissions import IsAuthenticated

from custom_user.models import User  # Adjust the import path based on your project structure
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)
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
            cancel_url='http://localhost:3000/payments/cancel',
            invoice_creation={"enabled": True},
        )

        data = {
            'checkout': checkout_session.url
        }

        return Response(data, content_type='application/json', status=status.HTTP_200_OK)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return JsonResponse({"message": "Something went wrong with the payment process"}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({"message": "Something went wrong with the payment process"}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        customer_email = session['customer_details']['email']

        send_mail(
            subject="Monthly subscription",
            message="Thank you very much for your purchase. Your monthly subscription is now active.",
            recipient_list=[customer_email],
            from_email="www.greetly.ch"
        )
        user_email = session['metadata']['user_email']
        user = User.objects.get(email=user_email)
        user.isSubscribed = True
        user.product_details['subscription_price'] = session['amount_total']
        user.product_details['subscription_plan'] = session['line_items']['data'][0]['price']['recurring']['interval']
        user.product_details['subscription_currency'] = session['line_items']['data'][0]['currency']
        user.product_details['subscription_id'] = session['subscription']

        user.save()

    return JsonResponse({"message": "Webhook received"}, status=200)




class CancelSubscription(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        data = json.loads(request.body.decode('utf-8'))
        user_email = data.get('email')

        subscription_id = data.get('subscription_id')

        response = stripe.Subscription.delete(
            subscription_id,
        )

        if response.cancellation_details:
            user = User.objects.get(email=user_email)

            user.isSubscribed = False
            user.product_details['subscription_price'] = ""
            user.product_details['subscription_plan'] = ""
            user.product_details['subscription_currency'] = ""
            user.product_details['subscription_id'] = ""

            user.save()

            return Response({'message': 'Subscription successfully canceled'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Failed to cancel subscription'}, status=status.HTTP_200_OK)
