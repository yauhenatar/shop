from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.urls import reverse
from .tasks import order_created

# from django.contrib.admin.views.decorators import staff_member_required
# from django.shortcuts import get_object_or_404
# from .models import Order
#
# @staff_member_required
# def admin_order_detail(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     return render(request,
#                   'admin/orders/order/detail.html',
#                   {'order': order})

def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            # очистка корзины
            cart.clear()

            # Сохранение заказа в сессии.
            request.session['order_id'] = order.id

            # Перенаправление на страницу оплаты.
            return redirect(reverse('payment:process'))

    else:
        form = OrderCreateForm()

        return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})