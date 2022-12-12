from django.db import models
from django.contrib.auth import get_user_model

from .managers import CustomerManager, DiscountsManager, OrderManager


User = get_user_model()


class Order(models.Model):
    STATUS = (('WORK', 'WORK'),
              ('START', 'START'),
              ('FINISH', 'FINISH'),
              ('ARCHIVE', 'ARCHIVE'))
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=256, choices=STATUS, null=False, default='START'
    )
    date_start = models.DateTimeField(auto_now_add=True)
    date_finish = models.DateTimeField(blank=True)
    address = models.CharField(max_length=256)

    objects = OrderManager()

    def __str__(self):
        return f'<{self.creator}>{self.product}'

    @property
    def customers(self):
        customers = list(self.customer_set.values_list('user', flat=True))
        cust_vals = list(self.customer_set.values_list('user', 'size'))
        sizes = list(self.customer_set.values_list('size', flat=True))
        size = sum(sizes)

        percent = self.product.discounts.discounts.get_percent(size)
        price = self.product.pph - (self.product.pph / 100) * percent
        self.product.discounts.discounts.get_all_percent()
        usernames = list(User.objects.filter(pk__in=customers).values_list('username', flat=True))
        out = zip(usernames, sizes, map(lambda x: "{:.2f}".format(round(price * x, 2)), sizes))
        return list(out)

    @property
    def order_size(self):
        return sum(list(Customer.objects.filter(order=self.pk).values_list('size', flat=True)))

    @property
    def discount(self):
        return self.product.discounts.discounts.get_percent(self.order_size)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    objects = CustomerManager()

    def __str__(self):
        return f'{self.user} {self.size}'


class Manufacture(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Contributor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Discount(models.Model):
    percent = models.IntegerField()
    size = models.IntegerField()
    objects = DiscountsManager()

    def __str__(self):
        return f'{self.percent}%{self.size}'


class DiscountSet(models.Model):
    discounts = models.ManyToManyField(Discount)

    def __str__(self):
        def frmt(discount):
            _, percent, size = discount
            return f'{percent}%{size}|'
        text = ''.join([x for x in map(frmt, self.discounts.values_list())])
        return f'|{text}'


class Product(models.Model):
    code = models.IntegerField(null=True)
    inn = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    manufacture = models.ForeignKey(Manufacture, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    ppv = models.IntegerField(default=0)
    pph = models.IntegerField(default=0)
    discounts = models.ForeignKey(DiscountSet, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} |{self.ppv}|{self.pph}{self.discounts}:{self.contributor}]'

    @property
    def prices(self):
        percent = self.discounts.discounts.get_all_percent()
        vals = self.discounts.discounts.get_values()
        # return map(lambda p: (p, self.pph - (self.pph/100) * p), percent)
        return map(lambda p: (p[0], p[1], "{:.2f}".format(self.pph - (self.pph/100) * p[0])), list(vals))


