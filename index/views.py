from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
import telebot


# Create your views here.
def index(request):
    all_products = models.Products.objects.all()
    categories = models.Categories.objects.all()
    return render(request, 'index.html', {'products':all_products, 'categories': categories})

def about(request):
    return HttpResponse('Мы типа работаем')

def contacts(request):
    return HttpResponse('+998971307995')

#детально про продукт
def details(request, pk):
    product = models.Products.objects.get(product_name=pk)

    return render(request, 'about_product.html', {'product': product})

def usercart(request):

    user_product = models.UserCart.objects.filter(user_id=request.user.id)

    total_amount = sum([total.quantity * total.product.product_price for total in user_product])

    return render(request, 'user_cart.html', {'product': user_product, 'total':total_amount})

#добавить продукт в корзину
def add_pr_to_cart(request, pk):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        user_id = request.user.id
        product_id = models.Products.objects.get(id=pk)

        if product_id.product_count > quantity:

        #Уменшение количество
            product_id.product_count -= quantity

            product_id.save()

            checker = models.UserCart.objects.filter(user_id=user_id, product=product_id)
            if not checker:
                models.UserCart.objects.create(user_id=user_id, product=product_id, quantity=quantity)
            
            else:
                pr_to_add = models.UserCart.objects.get(user_id=user_id, product=product_id)
                pr_to_add.quantity += quantity
                pr_to_add.save()

            return redirect('/')
        else:
            return redirect(f'/product/{product_id.product_name}')

def del_from_cart(request, pk):
    if request.method == 'POST':
        product_to_del = models.Products.objects.get(id=pk)

        user_cart = models.UserCart.objects.get(product = product_to_del, user_id=request.user.id)

        product_to_del.product_count += user_cart.quantity
        user_cart.delete()

        product_to_del.save()

        return redirect('/usercart')

def confirm_order(request, pk):
    if request.method == 'POST':
        user_cart = models.UserCart.objects.filter(user_id=request.user.id)

        full_message = 'Новый заказ:\n\n'

        for i in user_cart:
            full_message += f'Продукт:{i.product.product_name}: {i.quantity} шт\n'

        total = [i.product.product_price*i.quantity for i in user_cart]

        full_message += f'\n\nВсего за заказ: {sum(total)}'
        bot = telebot.TeleBot('5401237148:AAHVeNnfLP5ph1ic6vcL39Ie5l8y2GBPXxA')
        bot.send_message(1048798405, full_message)

        user_cart.delete()

        return redirect('/')