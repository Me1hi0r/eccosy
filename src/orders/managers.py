from django.db.models import Manager


class OrderManager(Manager):
    def update_status(self, pk, status):
        order = self.get(pk=pk)
        order.status = status.upper()
        order.save()


class CustomerManager(Manager):
    def get_order_size(self, order):
        return sum(self.filter(order=order).values_list('size', flat=True))

    def set_size(self, pk, size):
        customer = self.get(pk=pk)
        customer.size = size
        customer.save()

    def update_size(self, pk, size):
        customer = self.get(pk=pk)
        customer.size += size
        customer.save()

    def add_value(self, price):
        self.value = self.size * price


class DiscountsManager(Manager):
    def get_values(self):
        return self.values_list('percent', 'size')

    def get_all_percent(self):
        return list(self.values_list('percent', flat=True))

    def get_percent(self, size):
        percent = 0
        for [p, s] in self.get_values():
            if size >= s:
                percent = p
        return percent

    def get_percent_next(self, percent):
        next_percent = []
        next_size = []
        big_p = 0
        for [p, s] in self.get_values():
            if big_p < p:
                big_p = p
            if percent < p:
                next_percent.append(p)
                next_size.append(s)
        return min(next_percent) if next_percent else big_p, min(next_size) if next_size else 0
