from shop.celery import app
from django.core.mail import send_mail
from .models import Order


@app.task
def order_created(order_id): #отправка письма
    order = Order.objects.get(id=order_id)
    subject = 'Заказ {}'.format(order_id)
    message = '{},\n\nВы успешно разместили заказ.\
                Номер Вашего заказа {}.'.format(order.first_name,
                                             order.id)
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email])
    return mail_sent