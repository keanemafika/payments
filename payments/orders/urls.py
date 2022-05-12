from django.urls import path

from . import views
from orders.views import DownloadPDF, SaleView, EditSale, DeleteSale, ConfirmSale, PrintSaleReceipt

app_name = 'orders'

urlpatterns = [
    path('', views.home, name='home'),
    path('list-invoice/', views.list_invoice, name='list_invoice'),
    path('single-sale-details/<int:id>', views.single_sale, name='single_sale'),
    path('sale-receipt/<int:pk>', PrintSaleReceipt.as_view(), name="print_receipt"),
    path('pdf_download/<int:pk>', DownloadPDF.as_view(), name="pdf_download"),
    path('make-sale', SaleView.as_view(), name="make_sale"),
    path('confirm-sale/<int:pk>', ConfirmSale.as_view(), name="confirm_sale"),
    path('edit-sale/<int:pk>', EditSale.as_view(), name="edit_sale"),
    path('delete-sale/<int:pk>', DeleteSale.as_view(), name="delete_sale"),
]
