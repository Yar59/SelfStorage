import stripe

from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect
from main_site.models import Box, Subscription, User
from self_storage.settings import STRIPE_API_KEY


def make_payment(request, box_pk):
    user_id = request.user.id
    box = Box.objects.get(pk=box_pk)
    stripe.api_key = STRIPE_API_KEY

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': f'Вы арендуете бокс {box.number} по адресу {box.storage.address} сроком на 1 месяц',
                },
                'unit_amount': int(box.storage.rental_price) * 100,
            },
            'quantity': 1,
        }],
        mode='payment',
        metadata={
            'user_id': user_id,
            'box_pk': box_pk,
        },
        success_url=request.build_absolute_uri(reverse('payment:successed_payment')),
        cancel_url=request.build_absolute_uri(reverse('payment:cancelled_payment')),
    )

    return redirect(session.url, code=303)


def pay_success(request):
    stripe.api_key = STRIPE_API_KEY
    stripe_sessions = stripe.checkout.Session.list(limit=3)
    session = stripe_sessions['data'][0]
    if session['payment_status'] == 'paid':
        user_id = session['metadata']['user_id']
        box_pk = session['metadata']['box_pk']
        box = Box.objects.get(pk=box_pk)
        user = User.objects.get(id=user_id)
        Subscription.objects.get_or_create(
            box=box,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=30),
            type='Подписка',
            user=user
        )

    return render(request, 'success.html')


@login_required
def cancelled(request):
    return render(request, 'cancelled.html')

