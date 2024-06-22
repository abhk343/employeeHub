from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q
from django.http import JsonResponse
from .models import *
from .forms import *

# Item Views
class ItemListView(ListView):
    model = Item
    template_name = 'prod/item_list.html'
    context_object_name = 'items'

class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'prod/item_form.html'
    success_url = reverse_lazy('product:item_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Item'
        return context

class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'prod/item_form.html'
    success_url = reverse_lazy('product:item_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Item'
        return context

# Supplier Views
class SupplierListView(ListView):
    model = Supplier
    template_name = 'prod/supplier_list.html'
    context_object_name = 'suppliers'

class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'prod/supplier_form.html'
    success_url = reverse_lazy('product:supplier_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Supplier'
        return context

class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'prod/supplier_form.html'
    success_url = reverse_lazy('product:supplier_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Supplier'
        return context

# Product Views
class ProductListView(ListView):
    model = Product
    template_name = 'prod/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Product.objects.all()

        if query:
            queryset = queryset.filter(
                Q(Item__Item_Name__icontains=query) |
                Q(Supplier__Supplier_Name__icontains=query) |
                Q(Quantity__icontains=query) |
                Q(Price__icontains=query) |
                Q(Purchase_Date__icontains=query) |
                Q(Invoice_Number__icontains=query)
            )

        for product in queryset:
            product.total_price = product.Quantity * product.Price
            product.price_per_piece = product.Price / product.Quantity if product.Quantity != 0 else 0

        return queryset


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'prod/product_form.html'
    success_url = reverse_lazy('product:prd_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'prod/product_form.html'
    success_url = reverse_lazy('product:prd_list')

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('prd_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'message': 'Product deleted successfully'}, status=200)

# views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.http import JsonResponse
from django.db.models import Q
from .models import Stock_in
from .forms import StockInForm

class StockInView(ListView):
    model = Stock_in
    template_name = 'prod/stock_in.html'
    context_object_name = 'stock_entries'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(employee__Name__icontains=query) |
                Q(item__Item_Name__icontains=query) |
                Q(issue_date__icontains=query)
            )
        return queryset

class StockInCreateView(CreateView):
    model = Stock_in
    form_class = StockInForm
    template_name = 'prod/stock_create.html'
    success_url = reverse_lazy('product:stock_in_list')

class StockInUpdateView(UpdateView):
    model = Stock_in
    form_class = StockInForm
    template_name = 'prod/stock_create.html'
    success_url = reverse_lazy('stock_in_list')

class StockInDeleteView(DeleteView):
    model = Stock_in
    success_url = reverse_lazy('stock_in_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'message': 'Stock entry deleted successfully'}, status=200)

from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Sum
from .models import Item, Product, Stock_in

class RemainingStockView(TemplateView):
    template_name = 'prod/remaining_stock.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Item.objects.all()

        item_data = []
        for item in items:
            total_purchased = Product.objects.filter(Item=item).aggregate(total=Sum('Quantity'))['total'] or 0
            total_issued = Stock_in.objects.filter(item=item).aggregate(total=Sum('Quantity'))['total'] or 0
            remaining_stock = total_purchased - total_issued

            item_data.append({
                'item': item,
                'total_purchased': total_purchased,
                'total_issued': total_issued,
                'remaining_stock': remaining_stock,
            })

        context['item_data'] = item_data
        return context
