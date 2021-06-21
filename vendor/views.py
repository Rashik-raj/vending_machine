import vendor
from django.http import request
from django.shortcuts import render, get_object_or_404
from django.http import request
from .models import *
from django.contrib import messages
# Create your views here.

def test(request):
    vendor = get_object_or_404(Vendor, id=1)
    products = Product.objects.filter(vendor=vendor.id)
    context = {
        'vendor': vendor,
        'products': products,
    }
    if request.method == 'POST':
        name = request.POST['name']
        product = request.POST['product']
        quantity = request.POST['quantity']
        cash = request.POST['coin']
        transaction_type = request.POST['transaction_type']

        if transaction_type not in ['Purchase', 'Refund']:
            messages.error(request, 'Invalid Transaction Type')
            return render(request, 'home.htm', context)
        if transaction_type == 'Refund':
            cash = 0
        if not name or not product or not quantity or not cash:
            messages.error(request, 'Please Fill Up The Form')
            return render(request, 'home.htm', context)
        try:
            quantity = int(quantity)
            cash = int(cash)
        except:
            messages.error(request, 'Invalid Quantity or Cash')
            return render(request, 'home.htm', context)
        vendor_obj = Vendor.objects.get(id=1)
        product_obj = Product.objects.get(id=product)
        total_cost = product_obj.price * int(quantity)
        if transaction_type == 'Purchase':
            if quantity > product_obj.stock:
                messages.error(request, 'Product out of stock')
                return render(request, 'home.htm', context)
            if cash < total_cost:
                messages.error(request, 'Insufficient Cash')
                return render(request, 'home.htm', context)
            if (cash - total_cost) > vendor.account.balance:
                messages.error(request, 'Insufficient Change to return')
                return render(request, 'home.htm', context)
            perform_purchase(name, product_obj, quantity, cash, vendor_obj)
            messages.success(request, 'Purchase Successfull')
        else:
            if vendor.account.balance < total_cost:
                messages.info(request, 'Insufficient Cash, cannot be refunded at the moment')
                return render(request, 'home.htm', context)
            perform_refund(name, product_obj, quantity, vendor_obj)
            messages.success(request, 'Refund Successfull')
    return render(request, 'home.htm', context)

def perform_purchase(name, product, quantity, cash, vendor):
    transaction = Transaction(name=name, product=product, quantity=quantity, amount=cash, vendor=vendor, type='Purchase')
    transaction.save()
    product.stock -= quantity
    product.save()
    account = vendor.account
    account.balance += transaction.total_amount
    account.save()


def perform_refund(name, product, quantity, vendor):
    transaction = Transaction(name=name, product=product, quantity=quantity, amount=0, vendor=vendor, type='Refund')
    transaction.save()
    product.stock += quantity
    product.save()
    account = vendor.account
    account.balance -= transaction.total_amount
    account.save()
