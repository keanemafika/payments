from django.shortcuts import render, redirect, HttpResponse, reverse, get_object_or_404
from .forms import InvoiceForm, InvoiceSearchForm, SaleConfirmForm, SaleConfirmForm
from .models import Invoice
from django.views import View
from pay.views import render_to_pdf
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView



# Create your views here.
class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if (not self.request.user.is_authenticated):
            return redirect_to_login(self.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():
            return redirect('/')
        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)


class RedirectToPreviousMixin:

    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']




@login_required
def home(request):
    if request.user.groups.filter(name='Payments').exists():
        title = 'Welcome: This is the Home Page'
        context = {
            "title": title,
        }
        return render(request, "orders/home.html", context)
    else:
        return redirect('/')


@login_required
def single_sale(request, id):
    if request.user.groups.filter(name='Payments').exists():
        queryset = Invoice.objects.get(id=id)
        context = {
            "queryset": queryset,
        }
        return render(request, "orders/single-sale.html", context)
    else:
        return redirect('/')

class ConfirmSale(SuccessMessageMixin, UpdateView):
    raise_exception = False
    redirect_field_name = 'next'
    model = Invoice
    template_name = 'orders/confirm-sale.html'
    form_class = SaleConfirmForm
    success_message = 'Sale Succesfull!'

    def get_form_kwargs(self):
        kwargs = super(ConfirmSale, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("orders:print_receipt", kwargs={"pk": pk})

    def form_valid(self, form):
        form.instance.confirmed = True
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class SaleView(CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'orders/add_invoice.html'

    def get_success_url(self):
        return reverse("orders:confirm_sale", args=(self.object.id,))


class EditSale(RedirectToPreviousMixin, SuccessMessageMixin, UpdateView):
    raise_exception = False
    redirect_field_name = 'next'
    model = Invoice
    template_name = 'orders/edit-sale.html'
    form_class = InvoiceForm
    success_message = 'The sale has been edited and is ready for confirmation'


class DeleteSale(UserAccessMixin, SuccessMessageMixin, DeleteView):
    success_message = 'Sale cancelled succesfully!'
    raise_exception = False
    permission_required = 'orders.delete_sale'
    redirect_field_name = 'next'
    model = Invoice
    template_name = 'orders/sale-delete.html'
    # form_class = AnnouncementForm
    success_url = reverse_lazy('orders:make_sale')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteSale, self).delete(request, *args, **kwargs)


class PrintSaleReceipt(DetailView):
    model = Invoice
    template_name = 'orders/print-sale-receipt.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PrintSaleReceipt, self).get_context_data(*args, **kwargs)

        invoice = get_object_or_404(Invoice, id=self.kwargs['pk'])

        context["invoice"] = invoice
        return context


@login_required
def add_invoice(request):
    if request.user.groups.filter(name='Payments').exists():
        form = InvoiceForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('orders:list_invoice')
        context = {
            "form": form,
            "title": "New Invoice",
        }
        return render(request, "orders/add_invoice.html", context)
    else:
        return redirect('/')


@login_required
def list_invoice(request):
    form = InvoiceSearchForm(request.POST or None)
    queryset = Invoice.objects.all().order_by('-invoice_date')
    p = Paginator(queryset, 10)
    page_num = request.GET.get('page', 1)

    try:
        queryset = p.page(page_num)
    except EmptyPage:
        queryset = p.page(1)
    context = {
        'queryset': queryset,
    }
    context = {
        "queryset": queryset,
        "form": form,
    }
    if request.method == 'POST':
        queryset = Invoice.objects.filter(
            invoice_number__icontains=form['invoice_number'].value(), name__icontains=form['name'].value())
        context = {
            "form": form,
            "queryset": queryset,
        }
    return render(request, "orders/list_item.html", context)


class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        data = {}
        data['sale'] = Invoice.objects.get(id=self.kwargs['pk'])
        pdf = render_to_pdf('orders/pdf_template.html', data)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % ("12341231")
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
