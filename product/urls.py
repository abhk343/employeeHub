from django.urls import path
from .views import *

urlpatterns = [
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
]
