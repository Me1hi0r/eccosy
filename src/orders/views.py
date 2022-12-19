from django.shortcuts import render, redirect
from django.views import View
from .forms import OrderCreationForm, AddSizeForm
from .models import Product, Order, Customer


class MyOrder(View):
    def get(self, req):
        orders = Order.objects.filter(creator=req.user)
        join_orders = Customer.objects.filter(user=req.user)
        return render(req, 'order/user.html', {'orders': orders, 'join_orders': [o.order for o in join_orders]})


class ListOrder(View):
    def get(self, req):
        orders = Order.objects.all()
        products = Product.objects.all()
        return render(req, 'order/order.html', {'orders': orders, 'products': products})


class CreateOrder(View):
    template = 'order/create.html'

    def get(self, req, pk):
        form = OrderCreationForm()
        return render(req, self.template, {'form': form})

    def post(self, req, pk):
        form = OrderCreationForm(req.POST)
        if not form.is_valid():
            return render(req, self.template, {'form': form})
        order = Order(product=Product.objects.get(pk=pk),
                      creator=req.user,
                      status='WORK',
                      date_finish=form.cleaned_data['date_finish'],
                      comment=form.cleaned_data['comment'])
        order.save()
        Customer(user=req.user, order=order, size=form.cleaned_data['size']).save()
        return redirect('order:detail', order.id)


class ShowOrder(View):
    def get(self, req, pk):

        def price_patch(prc, customers):
            def add_value(customer):
                customer.value = customer.size * prc
                return customer
            return [add_value(customer) for customer in customers]

        order = Order.objects.get(pk=pk)
        bayers = Customer.objects.filter(order=order)
        order_size = Customer.objects.get_order_size(order)
        percent = order.product.discounts.discounts.get_percent(order_size)
        percent_next, size_next = order.product.discounts.discounts.get_percent_next(percent)
        price = order.product.pph - (order.product.pph / 100) * percent
        context = {'bayers': price_patch(price, bayers),
                   'order': order,
                   'az': order_size,
                   'p': percent,
                   'price': "{:.2f}".format(price),
                   'percent': percent_next,
                   'add': size_next - order_size}
        return render(req, 'order/detail.html', context)


class ChangeOrderStatus(View):
    def get(self, req, pk, status):
        Order.objects.update_status(pk, status.upper())
        return redirect('order:list')


class DeleteOrder(View):
    def get(self, req, pk):
        Order.objects.get(pk=pk).delete()
        return redirect('order:list')


class AddCustomer(View):
    template = 'order/append.html'

    def get(self, req, pk):
        form = AddSizeForm()
        return render(req, self.template, {'form': form})

    def post(self, req, pk):
        form = AddSizeForm(req.POST)
        if not form.is_valid():
            return render(req, self.template, {'form': form})
        form.cleaned_data['user'] = req.user
        form.cleaned_data['order'] = Order.objects.get(pk=pk)
        if Customer.objects.filter(order=pk, user=req.user):
            customer = Customer.objects.get(order=pk, user=req.user)
            customer.size = customer.size + form.cleaned_data['size']
        else:
            customer = Customer(**form.cleaned_data)
        customer.save()
        return redirect('order:detail', pk)


class ChangeCustomer(View):
    template = 'order/change.html'

    def get(self, req, pk, ck):
        form = AddSizeForm(initial={'size': Customer.objects.get(pk=ck).size})
        return render(req, self.template, {'form': form})

    def post(self, req, pk, ck):
        form = AddSizeForm(req.POST)
        if not form.is_valid():
            return render(req, self.template, {'form': form})
        Customer.objects.set_size(ck, form.cleaned_data['size'])
        return redirect('order:detail', pk)


class DropCustomer(View):
    def get(self, req, pk, ck):
        Customer.objects.get(pk=ck).delete()
        return redirect('order:detail', pk)
