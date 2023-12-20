from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.shortcuts import HttpResponseRedirect
from django.views.generic.list import ListView

from orders.forms import OrderForm
from common.views import TitleMixin
from orders.models import Order
from products.models import Basket


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'UPGrade PC - Заказы'
    queryset = Order.objects.all()
    ordering = '-created'

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'UPGrade PC - Оформление заказа'

    def post(self, request, *args, **kwargs):
        if Basket.objects.filter(user=request.user.id):
            super(OrderCreateView, self).post(request, *args, **kwargs)
            Order.objects.filter(initiator=request.user.id).last().update_after_payment()
            return HttpResponseRedirect(reverse_lazy('orders:order_success'))

        return HttpResponseRedirect(reverse_lazy('orders:order_canceled'))

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'UPGrade PC - Заказ #{self.object.id}'
        return context


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'



class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'UPGrade PC - Спасибо за заказ!'
