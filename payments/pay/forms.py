from django import forms
from pay.models import IndividualPayment, ClearanceForStudent, Level, Classroom
from django.contrib.auth.models import User
from pay.models import Profile


class IndividualPaymentForm(forms.ModelForm):
    class Meta:
        model = IndividualPayment
        fields = ('profile', 'currency', 'particular', 'term', 'cashier', 'month', 'actual_amount_paid',
                  'amount_paid', 'phone_number', 'address', 'client_name')

        widgets = {
            'profile': forms.Select(attrs={'class': 'form-control col-12'}),
            'month': forms.Select(attrs={'class': 'form-control col-12'}),
            'currency': forms.Select(attrs={'class': 'form-control col-12'}),
            'term': forms.Select(attrs={'class': 'form-control col-12'}),
            'particular': forms.Select(attrs={'class': 'form-control col-12'}),
            'address': forms.TextInput(attrs={'class': 'form-control col-12'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control col-12'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control col-12'}),
            'actual_amount_paid': forms.NumberInput(attrs={'class': 'form-control col-12'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control col-12'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(IndividualPaymentForm, self).__init__(*args, **kwargs)
        self.fields['cashier'].initial = self.user.profile
        self.fields['cashier'].disabled = True
        self.fields['cashier'].widget = forms.HiddenInput()


class IndividualPaymentConfirmForm(forms.ModelForm):
    class Meta:
        model = IndividualPayment
        fields = ('confirmed',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(IndividualPaymentConfirmForm, self).__init__(*args, **kwargs)
        self.fields['confirmed'].initial = True
        self.fields['confirmed'].disabled = True
        self.fields['confirmed'].widget = forms.HiddenInput()


class ClearanceForStudentForm(forms.ModelForm):
    class Meta:
        model = ClearanceForStudent
        fields = ('cleared',)

    def __init__(self, *args, **kwargs):
        super(ClearanceForStudentForm, self).__init__(*args, **kwargs)
        self.fields['cleared'].label = "Tick box to clear student"


class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'classroom', 'age', 'level', 'address', 'cell', 'tell', 'gender', 'user')

        widgets = {
            'profile': forms.Select(attrs={'class': 'form-control col-12'}),
            'gender': forms.Select(attrs={'class': 'form-control col-12'}),
            'classroom': forms.Select(attrs={'class': 'form-control col-12'}),
            'level': forms.Select(attrs={'class': 'form-control col-12'}),
            'address': forms.TextInput(attrs={'class': 'form-control col-12'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control col-12'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control col-12'}),
            'age': forms.NumberInput(attrs={'class': 'form-control col-12'}),
            'cell': forms.NumberInput(attrs={'class': 'form-control col-12'}),
            'tell': forms.NumberInput(attrs={'class': 'form-control col-12'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CompleteProfileForm, self).__init__(*args, **kwargs)
        self.fields['user'].initial = self.user
        self.fields['user'].disabled = True
        self.fields['level'].queryset = Level.objects.exclude(slug='admin-level')
        self.fields['classroom'].queryset = Classroom.objects.exclude(slug='admin-9')
        # self.fields['user'].widget = forms.HiddenInput()
