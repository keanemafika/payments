from django.db import models
from django.contrib.auth.models import User
import random
from django.db import IntegrityError
from datetime import datetime, date
from django.urls import reverse


class Year(models.Model):
    title = models.IntegerField()
    status = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.title}'


class Term(models.Model):
    title = models.CharField(max_length=15)
    slug = models.SlugField(max_length=15)
    year = models.ForeignKey(Year, null='False', blank=False,
                             on_delete=models.CASCADE, related_name='terms_of_year')
    total_days = models.IntegerField(null='False', blank=False)
    status = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            self.slug = ''.join(str(random.randint(0, 9)) for _ in range(8))
            super().save(*args, **kwargs)
        except IntegrityError:
            self.save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} - {self.year}'


class Gender(models.Model):
    title = models.CharField(max_length=10, null='False', blank=False,)
    created_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title


class ClusterLevel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, null='False', blank=False,)
    created_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=100)
    clusterlevel = models.ForeignKey(ClusterLevel, on_delete=models.CASCADE,
                              null='False', blank=False)
    slug = models.SlugField(max_length=50, null='False', blank=False,)
    created_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


def current_year():
    return date.today().year


class Classroom(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True, null='False', blank=False,)
    level = models.ForeignKey(Level, on_delete=models.CASCADE,
                              null=False, blank=False, default="")
    year = models.IntegerField(default=current_year())
    created_on = models.DateTimeField(default=datetime.now)

    def get_absolute_url(self):
        return reverse('pay:classroom_status', args=[self.slug])

    def __str__(self):
        return self.title  + f' (Level: {self.level.name})'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25, null='False', default='New Profile')
    last_name = models.CharField(max_length=15, null='False', blank=False,)
    address = models.CharField(max_length=50, null='True', blank=True,)
    gender = models.ForeignKey(Gender, null='False', blank=False, on_delete=models.CASCADE)
    age = models.IntegerField(null='False', blank=False)
    tell = models.IntegerField(null='True', blank=True, default=None)
    cell = models.IntegerField(null='True', blank=True, default=None)
    level = models.ForeignKey(Level, null='False', blank=False, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, null='False', blank=False,
                                  on_delete=models.CASCADE, related_name='profiles_of_classroom')
    is_admin_pay = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}' + ',   Name:' + f'{self.first_name}' + ' ' + f'{self.last_name}'


class ClearanceForStudent(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null='False', blank=False)
    term = models.ForeignKey(Term, null='False', blank=False, on_delete=models.CASCADE)
    cleared = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.term}' + '-' + f'{self.profile}' + '_' + f'{self.cleared}'


class FeesForTerm(models.Model):
    term = models.ForeignKey(Term, null='False', blank=False, on_delete=models.CASCADE)
    clusterlevel = models.ForeignKey(ClusterLevel, null='False', blank=False, on_delete=models.CASCADE)
    amount = models.IntegerField(null='True', blank=True)
    created_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.term}' + '_' + f'{self.amount}'


class GroceriesForTerm(models.Model):
    term = models.ForeignKey(Term, null='True', blank=True, on_delete=models.CASCADE)
    clusterlevel = models.ForeignKey(ClusterLevel, null='False', blank=False, on_delete=models.CASCADE)
    amount = models.IntegerField(null='True', blank=True)
    created_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.term}' + '_' + f'{self.amount}'


class IndividualPayment(models.Model):


    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(confirmed=True)

    Swipe = 'Swipe'
    USD = 'USD'
    Rand = 'Rand'
    Tuition = 'Tuition'
    Groceries = 'Groceries'
    Development = 'Development'
    Online_Learning = 'Online Learning'
    Reg_Fee = 'Registration Fee'
    Bus_Levy = 'Bus Levy'
    OPTIONS = [
        (Swipe, 'RTGS Swipe'),
        (USD, 'USD'),
        (Rand, 'Rand'),
    ]
    particular_OPTIONS = [
        (Tuition, 'Tuition'),
        (Groceries, 'Groceries'),
        (Development, 'Development'),
        (Online_Learning, 'Online Learning'),
        (Bus_Levy, 'Bus Levy'),
        (Reg_Fee, 'Registration Fee'),
    ]
    January = 'January'
    February = 'February'
    March = 'March'
    April = 'April'
    May = 'May'
    June = 'June'
    July = 'July'
    August = 'August'
    September = 'September'
    October = 'October'
    Novemver = 'Novemver'
    December = 'December'

    month_OPTIONS = [
        (January, 'January'),
        (February, 'February'),
        (March, 'March'),
        (April, 'April'),
        (May, 'May'),
        (June, 'June'),
        (July, 'July'),
        (August, 'August'),
        (September, 'September'),
        (October, 'October'),
        (Novemver, 'Novemver'),
        (December, 'December'),
    ]
    currency = models.CharField(max_length=10, choices=OPTIONS)
    particular = models.CharField(max_length=100, choices=particular_OPTIONS)
    month = models.CharField(max_length=100, choices=month_OPTIONS, null='True', blank=True)
    client_name = models.CharField(null='False', blank=False, max_length=30)
    address = models.CharField(null='True', blank=True, max_length=50, default="")
    phone_number = models.IntegerField(null='True', blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null='False', blank=False)
    cashier = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                null='False', blank=False, related_name='profile_cashier')
    term = models.ForeignKey(Term, on_delete=models.CASCADE, null='False',
                             blank=False, related_name='payments_of_terms')
    amount_paid = models.IntegerField(null='False', blank=False)
    actual_amount_paid = models.IntegerField(null='True', blank=True)
    created_on = models.DateTimeField(default=datetime.now)
    objects = models.Manager() #default manager
    newmanager = NewManager() #custom manager
    confirmed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('pay:single_student_details', args=[self.id])

    def __str__(self):
        return f'{self.profile.first_name}' + '-' + f'{self.profile.last_name}' + '-' + self.profile.user.username + '-' + f'{self.profile.classroom.title}' + '-class'
