from django.db import models
from myshop.models import Product

class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name = 'Имя')
    last_name = models.CharField(max_length=50, verbose_name = 'Фамилия')
    email = models.EmailField()
    address = models.CharField(max_length=250, verbose_name = 'Адрес')
    postal_code = models.CharField(max_length=20, verbose_name = 'Почтовый индекс')
    city = models.CharField(max_length=100, verbose_name = 'Город')
    created = models.DateTimeField(auto_now_add=True, verbose_name = 'Добавлен')
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Обновлён')
    paid = models.BooleanField(default=False, verbose_name = 'Оплачен')
    braintree_id = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity