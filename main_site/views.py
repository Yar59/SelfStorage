from datetime import timedelta, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Count, Max
from django.db.models import F
from django.contrib.auth import authenticate, login, logout

from .models import *
from .forms import *
from .mailer import *


def show_main_page(request):
    storage = Storage.objects.annotate(boxes_count=Count('boxes')).order_by('?').first()
    free_boxes = storage.boxes.free()
    box_max_height = free_boxes.aggregate(box_max_height=Max('height'))['box_max_height']
    storage = {
        'address': storage.address,
        'temperature': storage.temperature,
        'max_height': box_max_height,
        'rental_price': storage.rental_price,
        'total_boxes': storage.boxes_count,
        'free_boxes': free_boxes.count(),
        'images': storage.images
    }

    return render(request, template_name='index.html', context=storage)


@login_required
def show_boxes(request):
    storages = Storage.objects.prefetch_related('boxes')
    context = {'storages': {}}
    for storage in storages:
        free_boxes = storage.boxes.free().annotate(volume=F('width')*F('length')*F('height')).annotate(square=F('width')*F('length'))
        max_height = free_boxes.aggregate(box_max_height=Max('height'))['box_max_height']
        context['storages'][storage.pk] = {
            'info': storage,
            'free_boxes': free_boxes,
            'boxes_vol_to_3': free_boxes.filter(volume__lt=3),
            'boxes_vol_to_10': free_boxes.filter(volume__lt=10),
            'boxes_vol_from_10': free_boxes.filter(volume__gte=10),
            'max_height': max_height
        }

    return render(request, template_name='boxes.html', context=context)


@login_required
def show_my_rent(request):
    user = request.user

    subscriptions = Subscription.objects\
        .filter(user=user)\
        .prefetch_related('box')
    print(subscriptions)
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Ваш профиль успешно обновлен.')
            return redirect('main_site:my_rent')
        else:
            messages.error(request, 'Заполните все поля')
    else:
        user_form = UserProfileForm(instance=request.user)

    return render(request, template_name='my-rent.html', context={
        'subscriptions': subscriptions,
        'user_form': user_form,
        'payment_soon': (datetime.now() + timedelta(5)).date,
        'now': datetime.now().date
    })


def show_faq(request):
    return render(request, template_name='faq.html', context={})


def login_view(request):
    if request.method == 'POST':

        user = authenticate(email=request.POST['EMAIL'], password=request.POST['PASSWORD'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('main_site:my_rent')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')


def register_user(request):
    if request.method == 'POST':
        print('dict', request.POST)
        try:
            User.objects.get(email=request.POST['EMAIL_CREATE'])
            return HttpResponse('This email is already taken')
        except User.DoesNotExist:
            User.objects.create_user(email=request.POST['EMAIL_CREATE'], password=request.POST['PASSWORD_CREATE'])

        user = authenticate(request, email=request.POST['EMAIL_CREATE'], password=request.POST['PASSWORD_CREATE'])
        if user is not None:
            login(request, user)
        return redirect('main_site:main')


def logout_view(request):
    logout(request)

    return redirect('main_site:main')


@login_required
def open_box(request, box_id):
    user = request.user
    try:
        subscription = Subscription.objects.get(user=user, box__id=box_id, )
    except ObjectDoesNotExist:
        return HttpResponse('Это не Ваш бокс или срок аренды окончен')
    box_number = subscription.box.number
    qr_link = get_qr_link(box_number)
    html_content = f'''
    <h1>Ваш QR для открытия бокса №{box_number}</h1>
    <img src="{qr_link}">
    '''
    send_email(
        f'QR для открытия бокса №{box_number}',
        user.email,
        text_content=f'Привет,{user.username}',
        html_content=html_content,
    )
    return HttpResponse(html_content)