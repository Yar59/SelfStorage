from django.shortcuts import render
from .models import Storage, Box, Subscription
from django.db.models import Count, Max, Min


def show_main_page(request):
    storage = Storage.objects.annotate(boxes_count=Count('boxes')).order_by('?').first()
    boxes = storage.boxes.all().annotate(subscriptions_count=Count('subscriptions'))
    box_max_height = boxes.aggregate(box_max_height=Max('height'))['box_max_height']
    free_boxes = boxes.filter(subscriptions_count=0).count()
    storage = {
        'address': storage.address,
        'temperature': storage.temperature,
        'max_height': box_max_height,
        'rental_price': storage.rental_price,
        'total_boxes': storage.boxes_count,
        'free_boxes': free_boxes
    }

    return render(request, template_name='index.html', context=storage)


def show_boxes(request):
    return render(request, template_name='boxes.html', context={})


def show_my_rent(request):
    return render(request, template_name='my-rent.html', context={})


def show_faq(request):
    return render(request, template_name='faq.html', context={})