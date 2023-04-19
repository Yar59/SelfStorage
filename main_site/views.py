from django.shortcuts import render
from .models import Storage, Box, Subscription
from django.db.models import Count, Max
from django.db.models import F


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
        'free_boxes': free_boxes.count()
    }

    return render(request, template_name='index.html', context=storage)


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


def show_my_rent(request):
    return render(request, template_name='my-rent.html', context={})


def show_faq(request):
    return render(request, template_name='faq.html', context={})