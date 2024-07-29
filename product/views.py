from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q
from django.http import JsonResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

@login_required
def product_home(request):
    return render(request, 'prod/product_home.html')


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

from django.views.generic import ListView
from django.core.paginator import Paginator
from .models import Product
from .filters import *

class ProductListView(ListView):
    model = Product
    template_name = 'prod/product_list.html'
    context_object_name = 'products'
    paginate_by = 5  # Number of products per page

    def get_queryset(self):
        queryset = super().get_queryset()

        # Apply filtering using django-filter ProductFilter
        filter = ProductFilter(self.request.GET, queryset=queryset)
        queryset = filter.qs

        # Calculate additional properties for each product
        for product in queryset:
            product.total_price = product.Quantity * product.Price_per_piece  # Calculate total_price

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the filter form to the context
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())

        # Paginate queryset
        paginator = Paginator(context['filter'].qs, self.paginate_by)
        page = self.request.GET.get('page')
        products = paginator.get_page(page)
        context['products'] = products

        return context


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
# views.py

# views.py

from django.shortcuts import redirect
from django.views.generic.edit import FormView, CreateView
from django.urls import reverse_lazy
from .forms import DepartmentSelectForm, StockInForm
from .models import Stock_in
from employee.models import Employee, Department

from django.views.generic import TemplateView
from django.urls import reverse_lazy
from employee.models import Department

class DepartmentSelectView(TemplateView):
    template_name = 'prod/select_dept.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        department_id = request.POST.get('department')
        if department_id:
            return redirect(reverse_lazy('product:stock_in_create') + f'?department={department_id}')
        return self.get(request, *args, **kwargs)

from django.views.generic.edit import CreateView
from .models import Stock_in, Employee
from .forms import StockInForm
from django.urls import reverse_lazy

class StockInCreateView(CreateView):
    model = Stock_in
    form_class = StockInForm
    template_name = 'prod/stock_create.html'
    success_url = reverse_lazy('product:stock_in_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        department_id = self.request.GET.get('department')
        if department_id:
            kwargs['department_id'] = department_id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department_id = self.request.GET.get('department')
        if department_id:
            context['employees'] = Employee.objects.filter(Department_id=department_id)
        return context


from django.views.generic import ListView
from django.core.paginator import Paginator
from .models import Stock_in
from .filters import StockFilter  # Import your StockFilter

class StockInView(ListView):
    model = Stock_in
    template_name = 'prod/stock_in.html'
    context_object_name = 'stock_entries'  # Use 'stock_entries' for ListView
    paginate_by = 5  # Number of stock entries per page

    def get_queryset(self):
        queryset = super().get_queryset()

        # Apply filtering using StockFilter
        filter = StockFilter(self.request.GET, queryset=queryset)
        queryset = filter.qs

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the filter form to the context
        context['filter'] = StockFilter(self.request.GET, queryset=self.get_queryset())

        # Paginate the filtered queryset
        paginator = Paginator(context['filter'].qs, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['stock_entries'] = page_obj

        return context



import csv
from django.http import HttpResponse
from django.views.generic import View

class DownloadCSV(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="stock_data.csv"'

        writer = csv.writer(response)
        # Write headers
        writer.writerow(['Emp Code', 'Employee', 'Department', 'Item', 'Quantity', 'Issue Date'])

        # Write data rows
        for stock in Stock_in.objects.all():  # Adjust queryset as per your filtering needs
            writer.writerow([
                stock.employee.Emp_code,
                stock.employee,
                stock.employee.Department,
                stock.item,
                stock.Quantity,
                stock.issue_date,
            ])

        return response

    


class StockInUpdateView(UpdateView):
    model = Stock_in
    form_class = StockInForm
    template_name = 'prod/stock_create.html'
    success_url = reverse_lazy('product:stock_in_list')

class StockInDeleteView(DeleteView):
    model = Stock_in
    success_url = reverse_lazy('product:stock_in_list')

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

# views.py# views.py
from django.views.generic import ListView
from employee.models import Employee
from employee.filters import EmployeeFilter

class EmployeeListView(ListView):
    model = Employee
    template_name = 'prod/employee_stock_list.html'
    context_object_name = 'employees'
    paginate_by = None  # Disable pagination

    def get_queryset(self):
        # Return all employees
        return Employee.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Initialize the filterset with the current queryset
        filterset = EmployeeFilter(self.request.GET, queryset=self.get_queryset())
        
        # Apply the filter to the context queryset
        context['employees'] = filterset.qs
        
        # Add filterset for EmployeeStockFilter to context
        context['filterset'] = filterset
        
        return context

# views.py
# views.py
# views.py

from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Stock_in, Employee
# views.py

from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Stock_in, Employee

class EmployeeStockDetailView(DetailView):
    model = Stock_in
    template_name = 'prod/stock_rec.html'
    context_object_name = 'stocks'
    
    def get_object(self, queryset=None):
        employee_id = self.kwargs.get('employee_id')
        employee = get_object_or_404(Employee, Employee_id=employee_id)
        stocks = Stock_in.objects.filter(employee=employee)
        return stocks

