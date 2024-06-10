from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from .models import Item, Supplier
from .forms import ItemForm, SupplierForm

class ItemListView(ListView):
    model = Item
    template_name = 'prod/item_list.html'
    context_object_name = 'items'

class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'prod/item_form.html'
    success_url = reverse_lazy('item_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Item'
        return context

class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'prod/item_form.html'
    success_url = reverse_lazy('item_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Item'
        return context

class SupplierListView(ListView):
    model = Supplier
    template_name = 'prod/supplier_list.html'
    context_object_name = 'suppliers'

class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'prod/supplier_form.html'
    success_url = reverse_lazy('supplier_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Supplier'
        return context

class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'prod/supplier_form.html'
    success_url = reverse_lazy('supplier_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Supplier'
        return context

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Product
from .forms import ProductForm
from django.db.models import Q

class ProductListView(ListView):
    model = Product
    template_name = 'prod/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(
                Q(Item__Item_Name__icontains=query) |
                Q(Supplier__Supplier_Name__icontains(query)) |
                Q(Quantity__icontains(query)) |
                Q(Price__icontains(query)) |
                Q(Purchase_Date__icontains(query)) |
                Q(Invoice_Number__icontains(query))
            )
        return Product.objects.all()
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Product
from .forms import ProductForm

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'prod/product_form.html'
    success_url = '/success/'  # Replace with your success URL

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'prod/product_form.html'
    success_url = '/success/'  # Replace with your success URL
from django.http import JsonResponse
from django.views.generic import DeleteView
from django.urls import reverse_lazy

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('prod/production_list')  # Redirect to product list after successful deletion

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return JsonResponse({'message': 'Product deleted successfully'}, status=200)
