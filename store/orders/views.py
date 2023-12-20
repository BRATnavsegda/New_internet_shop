from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.shortcuts import HttpResponseRedirect

from orders.forms import OrderForm
from common.views import TitleMixin


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'UPGrade PC - Оформление заказа'

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)

        return HttpResponseRedirect(reverse_lazy('orders:order_canceled'))

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'UPGrade PC - Спасибо за заказ!'
