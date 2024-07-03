from django.urls import path
from .views import *

app_name = 'product'

urlpatterns = [
    path('prod_home/', product_home ,name="prod_home"),
    path('itin/', ItemCreateView.as_view(), name='add_item'),
    path('itv/', ItemListView.as_view(), name='item_list'),
    path('edit/<int:pk>/', ItemUpdateView.as_view(), name='edit_item'),
    path('stin/', SupplierCreateView.as_view(), name='add_supplier'),
    path('stv/', SupplierListView.as_view(), name='supplier_list'),
    path('sedit/<int:pk>/', SupplierUpdateView.as_view(), name='edit_supplier'),
    path('prd/', ProductListView.as_view(), name='prd_list'),
    path('prd/add/', ProductCreateView.as_view(), name='prd_add'),
    path('prd/edit/<int:pk>/', ProductUpdateView.as_view(), name='prd_edit'),
    path('prd/delete/<int:pk>/', ProductDeleteView.as_view(), name='prd_delete'),
    path('stock/', StockInView.as_view(), name='stock_in_list'),
    path('stock/add/', StockInCreateView.as_view(), name='stock_in_add'),
    path('stock/<int:pk>/edit/', StockInUpdateView.as_view(), name='stock_in_edit'),
    path('stock/<int:pk>/delete/', StockInDeleteView.as_view(), name='stock_in_delete'),
    path('remaining_stock/', RemainingStockView.as_view(), name='remaining_stock'),
    ]
