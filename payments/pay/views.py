from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from pay.models import IndividualPayment, Classroom, Profile, Term, Gender, FeesForTerm, GroceriesForTerm, ClearanceForStudent, ClusterLevel
from pay.forms import IndividualPaymentForm, ClearanceForStudentForm, IndividualPaymentConfirmForm, CompleteProfileForm
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.contrib.auth.models import User
import io
import csv
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required


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


def render_to_pdf(template_src, context_dict={}):
    if request.user.groups.filter(name='Payments').exists():
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None
    else:
        return redirect('/')


@login_required
def payments(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Payments').exists():
            individualpayment = IndividualPayment.newmanager.all().order_by('-created_on')[:5]
            context = {
                'individualpayment': individualpayment,
            }
            return render(request, 'pay/index.html', context)
        else:
            return redirect('/')

    else:
        return redirect('/admin/login')


@login_required
def make_payment(request):
    if request.user.groups.filter(name='Payments').exists():
        return render(request, 'pay/make-payment.html')
    else:
        return redirect('/')


@login_required
def all_transactions(request):
    if request.user.groups.filter(name='Payments').exists():
        individualpayment = IndividualPayment.newmanager.all().order_by('-created_on')
        p = Paginator(individualpayment, 10)
        page_num = request.GET.get('page', 1)

        try:
            individualpayment = p.page(page_num)
        except EmptyPage:
            individualpayment = p.page(1)
        context = {
            'individualpayment': individualpayment,
        }
        return render(request, 'pay/all-transactions.html', context)
    else:
        return redirect('/')


@login_required
def check_status(request):
    if request.user.groups.filter(name='Payments').exists():

        context = {
            'classroom_statuses': Classroom.objects.all(),
        }
        return render(request, 'pay/check-status.html', context)
    else:
        return redirect('/')


@login_required
def classroom_status(request, slug):
    if request.user.groups.filter(name='Payments').exists():
        get_classroom = Classroom.objects.get(slug=slug)
        get_all_users = Profile.objects.filter(classroom=get_classroom)
        context = {
            'get_classroom': get_classroom,
            'get_all_users': get_all_users,
        }
        return render(request, 'pay/class-status.html', context)
    else:
        return redirect('/')


@login_required
def single_student_details(request, username):
    if request.user.groups.filter(name='Payments').exists():
        get_user = User.objects.get(username=username)


        term_1_2022 = Term.objects.get(slug=42391862)
        term_2_2022 = Term.objects.get(slug=25075060)
        term_3_2022 = Term.objects.get(slug=46724868)
        clusterlevel = get_user.profile.level.clusterlevel
        feesforterm_1_2022 = FeesForTerm.objects.get(clusterlevel=clusterlevel, term=term_1_2022)
        feesforterm_2_2022 = FeesForTerm.objects.get(clusterlevel=clusterlevel, term=term_2_2022)
        feesforterm_3_2022 = FeesForTerm.objects.get(clusterlevel=clusterlevel, term=term_3_2022)

        try:
            get_clearance_for_term_1_2022 = ClearanceForStudent.objects.get(
                profile=get_user.profile, term=term_1_2022)
        except ClearanceForStudent.DoesNotExist:
            get_clearance_for_term_1_2022 = None

        try:
            get_clearance_for_term_2_2022 = ClearanceForStudent.objects.get(
                profile=get_user.profile, term=term_2_2022)
        except ClearanceForStudent.DoesNotExist:
            get_clearance_for_term_2_2022 = None

        if get_user.profile.level.clusterlevel.slug == "pre-school":
            groceriesforterm_1_2022 = GroceriesForTerm.objects.get(clusterlevel=clusterlevel, term=term_1_2022)
            groceriesforterm_2_2022 = GroceriesForTerm.objects.get(clusterlevel=clusterlevel, term=term_2_2022)
            groceriesforterm_3_2022 = GroceriesForTerm.objects.get(clusterlevel=clusterlevel, term=term_3_2022)


            # TERM 1 2022
            # All term payments
            all_term_1_payments = IndividualPayment.newmanager.filter(
                profile=get_user.profile, term=term_1_2022)



            # tuition Paid term 1 2022
            individualpayment_payments_for_term_1_2022 = IndividualPayment.newmanager.filter(
                profile=get_user.profile, particular='Tuition', term=term_1_2022)
            total_tuition_paid_term_1_2022 = sum(
                individualpayment_payments_for_term_1_2022.values_list('amount_paid', flat=True))
            tuition_balance_term_1_2022 = feesforterm_1_2022.amount - total_tuition_paid_term_1_2022

            # Bus levy
            bus_levy_payments = IndividualPayment.objects.filter(
                profile=get_user.profile,
                particular = 'Bus Levy',
                term = term_1_2022
            )
            bus_levy_payments_total = sum(bus_levy_payments.values_list('amount_paid', flat=True))
            bus_levy_balance_term_1_2022 = 30 - bus_levy_payments_total


            # groceries paid
            groceries_due_term_1_2022 = GroceriesForTerm.objects.get(term=term_1_2022)
            individualpayment_groceries_term_1_2022 = IndividualPayment.newmanager.filter(particular='Groceries', term=term_1_2022, profile=get_user.profile)
            total_groceries_paid_term_1_2022 = sum(
                individualpayment_groceries_term_1_2022.values_list('amount_paid', flat=True))

            groceries_balance_term_1_2022 = groceriesforterm_1_2022.amount - total_groceries_paid_term_1_2022

            # total balance Term 1 2022
            total_balance_term_1_2022 = tuition_balance_term_1_2022 + groceries_balance_term_1_2022 + bus_levy_balance_term_1_2022

            # TERM 2 2022

            # All term payments
            all_term_2_payments = IndividualPayment.newmanager.filter(
                profile=get_user.profile, term=term_2_2022)


            # tuition Paid term 2 2022
            individualpayment_payments_for_term_2_2022 = IndividualPayment.newmanager.filter(
                profile=get_user.profile, particular='Tuition', term=term_2_2022)
            total_tuition_paid_term_2_2022 = sum(
                individualpayment_payments_for_term_2_2022.values_list('amount_paid', flat=True))
            tuition_balance_term_2_2022 = feesforterm_1_2022.amount - total_tuition_paid_term_2_2022


            # Bus levy
            bus_levy_payments = IndividualPayment.objects.filter(
                profile=get_user.profile,
                particular = 'Bus Levy',
                term = term_2_2022
            )
            bus_levy_payments_total = sum(bus_levy_payments.values_list('amount_paid', flat=True))
            bus_levy_balance_term_2_2022 = 30 - bus_levy_payments_total



            # groceries paid
            groceries_due_term_2_2022 = GroceriesForTerm.objects.get(term=term_2_2022)
            individualpayment_groceries_term_2_2022 = IndividualPayment.newmanager.filter(particular='Groceries', term=term_2_2022, profile=get_user.profile)
            total_groceries_paid_term_2_2022 = sum(
                individualpayment_groceries_term_2_2022.values_list('amount_paid', flat=True))

            groceries_balance_term_2_2022 = groceriesforterm_1_2022.amount - total_groceries_paid_term_2_2022

            # total balance Term 2 2022
            total_balance_term_2_2022 = tuition_balance_term_2_2022 + groceries_balance_term_2_2022 + bus_levy_balance_term_2_2022
            context = {
                # TERM 1 2022
                'all_term_1_payments': all_term_1_payments,
                'get_clearance_for_term_1_2022': get_clearance_for_term_1_2022,
                'total_balance_term_1_2022': total_balance_term_1_2022,
                'groceries_balance_term_1_2022': groceries_balance_term_1_2022,
                'tuition_balance_term_1_2022': tuition_balance_term_1_2022,
                'bus_levy_balance_term_1_2022': bus_levy_balance_term_1_2022,
                'individualpayment_groceries_term_1_2022': individualpayment_groceries_term_1_2022,
                'individualpayment_tuition_term_1_2022': individualpayment_payments_for_term_1_2022,
                # TERM 2 2022
                'all_term_2_payments': all_term_2_payments,
                'get_clearance_for_term_2_2022': get_clearance_for_term_2_2022,
                'total_balance_term_2_2022': total_balance_term_2_2022,
                'groceries_balance_term_2_2022': groceries_balance_term_2_2022,
                'bus_levy_balance_term_2_2022': bus_levy_balance_term_2_2022,
                'tuition_balance_term_2_2022': tuition_balance_term_2_2022,
                'individualpayment_groceries_term_2_2022': individualpayment_groceries_term_2_2022,
                'individualpayment_tuition_term_2_2022': individualpayment_payments_for_term_2_2022,
                'get_user': get_user,
            }

            return render(request, 'pay/single-student-details.html', context)
        else:
            # TERM 1 2022
            # tuition Paid
            individualpayment_payments_for_term_1_2022 = IndividualPayment.newmanager.filter(
                profile=get_user.profile, particular='Tuition', term=term_1_2022)
            total_tuition_paid_term_1_2022 = sum(
                individualpayment_payments_for_term_1_2022.values_list('amount_paid', flat=True))
            tuition_balance_term_1_2022 = feesforterm_1_2022.amount - total_tuition_paid_term_1_2022


            # Bus levy
            bus_levy_payments = IndividualPayment.objects.filter(
                profile=get_user.profile,
                particular = 'Bus Levy',
                term = term_1_2022
            )
            bus_levy_payments_total = sum(bus_levy_payments.values_list('amount_paid', flat=True))
            bus_levy_balance_term_1_2022 = 50 - bus_levy_payments_total

            # total balance Term 1 2022
            total_balance_term_1_2022 = tuition_balance_term_1_2022

            # TERM 2 2022
            # tuition Paid
            individualpayment_payments_for_term_2_2022 = IndividualPayment.newmanager.filter(
                profile=get_user.profile, particular='Tuition', term=term_2_2022)
            total_tuition_paid_term_2_2022 = sum(
                individualpayment_payments_for_term_2_2022.values_list('amount_paid', flat=True))
            tuition_balance_term_2_2022 = feesforterm_1_2022.amount - total_tuition_paid_term_2_2022


            # Bus levy
            bus_levy_payments = IndividualPayment.objects.filter(
                profile=get_user.profile,
                particular = 'Bus Levy',
                term = term_2_2022
            )
            bus_levy_payments_total = sum(bus_levy_payments.values_list('amount_paid', flat=True))
            bus_levy_balance_term_2_2022 = 50 - bus_levy_payments_total

            # total balance Term 2 2022
            total_balance_term_2_2022 = tuition_balance_term_2_2022


            context = {
                # TERM 1 2022
                'get_clearance_for_term_1_2022': get_clearance_for_term_1_2022,
                'total_balance_term_1_2022': total_balance_term_1_2022,
                'tuition_balance_term_1_2022': tuition_balance_term_1_2022,
                'bus_levy_balance_term_1_2022': bus_levy_balance_term_1_2022,
                'individualpayment_tuition_term_1_2022': individualpayment_payments_for_term_1_2022,
                # TERM 2 2022
                'get_clearance_for_term_2_2022': get_clearance_for_term_2_2022,
                'total_balance_term_2_2022': total_balance_term_2_2022,
                'tuition_balance_term_2_2022': tuition_balance_term_2_2022,
                'bus_levy_balance_term_2_2022': bus_levy_balance_term_2_2022,
                'individualpayment_tuition_term_2_2022': individualpayment_payments_for_term_2_2022,
                'get_user': get_user,
            }

            return render(request, 'pay/single-student-details.html', context)
    else:
        return redirect('/')



class RedirectToPreviousMixin:

    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']


class ClearStudentView(SuccessMessageMixin, RedirectToPreviousMixin, UpdateView):
    model = ClearanceForStudent
    template_name = 'pay/clear-student.html'
    form_class = ClearanceForStudentForm
    redirect_field_name = 'next'
    success_message = 'This Student has been cleared'


class PaymentView(UserAccessMixin, PermissionRequiredMixin , CreateView):
    model = IndividualPayment
    form_class = IndividualPaymentForm
    template_name = 'pay/make-payment.html'
    permission_required = ('pay.change_individualpayment', 'pay.view_individualpayment', 'pay.add_individualpayment', 'pay.delete_individualpayment')

    def get_form_kwargs(self):
        kwargs = super(PaymentView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse("pay:confirm_payment", args=(self.object.id,))


class PrintReceipt(UserAccessMixin, PermissionRequiredMixin , DetailView):
    model = IndividualPayment
    template_name = 'pay/print-receipt.html'
    permission_required = ('pay.change_individualpayment', 'pay.view_individualpayment', 'pay.add_individualpayment', 'pay.delete_individualpayment')

    def get_context_data(self, *args, **kwargs):
        context = super(PrintReceipt, self).get_context_data(*args, **kwargs)

        individualpayment = get_object_or_404(IndividualPayment, id=self.kwargs['pk'])

        context["individualpayment"] = individualpayment
        return context


class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        data = {}
        context = {
            'payment': IndividualPayment.newmanager.get(id=self),
        }
        pdf = render_to_pdf('pay/pdf_template.html', data, context)
        return HttpResponse(pdf, content_type='application/pdf')


# Automaticly downloads to PDF filecurrency


class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        data = {}
        data['payment'] = IndividualPayment.newmanager.get(id=self.kwargs['pk'])
        pdf = render_to_pdf('pay/pdf_template.html', data)
        payment_for_id = IndividualPayment.newmanager.get(id=self.kwargs['pk'])
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % (f'{payment_for_id.id}-{payment_for_id.profile.user.username}')
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response


class ConfirmPayment(UserAccessMixin, PermissionRequiredMixin , SuccessMessageMixin, UpdateView):
    raise_exception = False
    redirect_field_name = 'next'
    model = IndividualPayment
    template_name = 'pay/confirm-payment.html'
    form_class = IndividualPaymentConfirmForm
    success_message = 'Payment Succesfull!'
    permission_required = ('pay.change_individualpayment', 'pay.view_individualpayment', 'pay.add_individualpayment', 'pay.delete_individualpayment')

    def get_form_kwargs(self):
        kwargs = super(ConfirmPayment, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("pay:print_receipt", kwargs={"pk": pk})

    def form_valid(self, form):
        form.instance.confirmed = True
        return super().form_valid(form)


class EditPayment(UserAccessMixin, PermissionRequiredMixin , SuccessMessageMixin, RedirectToPreviousMixin, UpdateView):
    raise_exception = False
    redirect_field_name = 'next'
    model = IndividualPayment
    template_name = 'pay/edit-payment.html'
    form_class = IndividualPaymentForm
    success_message = 'Your payment had been edited and is ready for confirmation'
    permission_required = ('pay.change_individualpayment', 'pay.view_individualpayment', 'pay.add_individualpayment', 'pay.delete_individualpayment')

    def get_form_kwargs(self):
        kwargs = super(EditPayment, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class DeletePayment(UserAccessMixin, SuccessMessageMixin, DeleteView):
    success_message = 'Payment cancelled succesfully!'
    raise_exception = False
    permission_required = ('pay.change_individualpayment', 'pay.view_individualpayment', 'pay.add_individualpayment', 'pay.delete_individualpayment')
    redirect_field_name = 'next'
    model = IndividualPayment
    template_name = 'pay/payment-delete.html'
    # form_class = AnnouncementForm
    success_url = reverse_lazy('pay:home')


    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeletePayment, self).delete(request, *args, **kwargs)




@permission_required('user.add_user')
def contact_upload(request):
    template = "pay/contact_upload.html"

    prompt = {
        'order': 'Order should be what what'
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'asoCSV leyi!!')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        password = column[9]
        username = column[0]
        user = User(
            username=username,
            password=password,
        )
        user.set_password(password)
        user.save()
    context = {}
    return render(request, template, context)


@permission_required('profile.add_profile')
def profile_upload(request):
    template = "pay/contact_upload.html"

    prompt = {
        'order': 'Order should be what what'
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'asoCSV leyi!!')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        username = column[0]
        first_name = column[1]
        last_name = column[2]
        gender = column[3]
        age = column[4]
        classroom = column[5]
        position = column[6]
        surbub = column[7]
        is_teacher = column[8]
        get_user = User.objects.get(username=username)
        get_classroom = Classroom.objects.get(slug=classroom)
        obj, created = Profile.objects.update_or_create(
            user=get_user,
        )
        obj.user = get_user
        obj.first_name = first_name
        obj.last_name = last_name
        obj.age = age
        obj.gender = Gender.objects.get(id=gender)
        obj.classroom = get_classroom
        obj.level = get_classroom.level
        obj.position = position
        obj.is_teacher = is_teacher
        obj.save()
    context = {}
    return render(request, template, context)


@permission_required('pay.add_groceries_for_student')
def groceries_upload(request):
    template = "pay/contact_upload.html"

    prompt = {
        'order': 'Order should be what what'
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'asoCSV leyi!!')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        username = column[0]
        term = column[10]
        groceries = column[13]
        get_user = User.objects.get(username=username)
        obj, created = GroceriesForStudent.objects.update_or_create(
            user=get_user,
        )
        obj.term = Term.objects.get(slug=term)
        obj.amount = groceries
        obj.save()
    context = {}
    return render(request, template, context)


@permission_required('pay.add_feesforstudent')
def tuition_upload(request):
    template = "pay/contact_upload.html"

    prompt = {
        'order': 'Order should be what what'
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'asoCSV leyi!!')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        username = column[0]
        term = column[10]
        tuition = column[12]
        get_user = User.objects.get(username=username)
        obj, created = FeesForStudent.objects.update_or_create(
            user=get_user,
        )
        obj.term = Term.objects.get(slug=term)
        obj.amount = tuition
        obj.save()
    context = {}
    return render(request, template, context)


@permission_required('pay.add_clearancefosrstudent')
def clearance_upload(request):
    template = "pay/contact_upload.html"

    prompt = {
        'order': 'Order should be what what'
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'asoCSV leyi!!')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        username = column[0]
        term = column[10]
        clearance = column[13]
        get_user = User.objects.get(username=username)
        obj, created = ClearanceForStudent.objects.update_or_create(
            profile=get_user.profile,
        )
        obj.term = Term.objects.get(slug=term)
        obj.clearance = clearance
        obj.save()
    context = {}
    return render(request, template, context)


@permission_required('user.add_user')
def enrol_student(request):

    test = Profile.objects.last()
    test = test.user.username
    test = test[1:]
    test = int(test)
    test = test + 1
    # string = 'WASC'
    test = 'W' + f'{test}'
    context = {
        'test': test,
    }

    if request.method == "POST":
        password = request.POST['password']
        username = test
        user = User(
            username=username,
            password=password,
        )
        user.set_password(user.password)
        user.save()
        user = user
        messages.success(request, 'User Creation almost complete!!')
        return redirect("pay:complete_profile", user.profile.pk)
    else:
        return render(request, 'pay/enrol-student.html', context)


class CompleteProfile(SuccessMessageMixin, UpdateView):
    raise_exception = False
    redirect_field_name = 'next'
    model = Profile
    template_name = 'pay/complete-profile.html'
    form_class = CompleteProfileForm
    success_message = 'Profile Created'

    def get_form_kwargs(self):
        kwargs = super(CompleteProfile, self).get_form_kwargs()
        pk = self.kwargs["pk"]
        profile = Profile.objects.get(pk=pk)
        kwargs.update({'user': profile.user})
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(CompleteProfile, self).get_context_data(*args, **kwargs)

        pk = self.kwargs["pk"]
        profile = Profile.objects.get(pk=pk)

        context["user"] = profile.user
        return context

    def get_success_url(self):
        pk = self.kwargs["pk"]
        profile = Profile.objects.get(pk=pk)
        return reverse("pay:single_student_details", args=(profile.user.username,))


class EditStudentDetails(RedirectToPreviousMixin, SuccessMessageMixin, UpdateView):
    raise_exception = False
    redirect_field_name = 'next'
    model = Profile
    template_name = 'pay/complete-profile.html'
    form_class = CompleteProfileForm
    success_message = 'Student profile edited succesfully'

    def get_form_kwargs(self):
        kwargs = super(EditStudentDetails, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
