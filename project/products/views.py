# digital/views.py
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from .models import DigitalProduct

def download_product(request, order_id):
    """Самая простая функция скачивания"""
    # Здесь должна быть проверка заказа, но для простоты пропустим
    digital_product = get_object_or_404(DigitalProduct, id=order_id)
    
    response = FileResponse(digital_product.file.open())
    response['Content-Disposition'] = f'attachment; filename="{digital_product.file.name}"'
    return response