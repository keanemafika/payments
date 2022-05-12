from django.db import models
from datetime import datetime
from django.urls import reverse


class Invoice(models.Model):
    currency_type_choice = (
        ('Rand', 'Rand'),
        ('USD', 'USD'),
        ('RTGS', 'RTGS'),
    )
    product_type_choice = (
        ('Satchel ECD', 'Satchel ECD'),
        ('Satchel Primary', 'Satchel Primary'),
        ('Jersey', 'Jersey'),
        ('Sunhat', 'Sunhat'),
        ('Sports Wear', 'Sports Wear'),
        ('Anorak', 'Anorak'),
        ('Masks', 'Masks'),
        ('Shield', 'Shield'),
        ('Tie', 'Tie'),
        ('Blazer', 'Blazer'),
        ('Summer Uniform ECD', 'Summer Uniform ECD'),
        ('Winter Uniform ECD', 'Winter Uniform ECD'),
        ('Summer Dress Primary', 'Summer Dress Primary'),
        ('Summer Shirts Primary', 'Summer Shirts Primary'),
        ('Winter Shirts Primary', 'Winter Shirts Primary'),
        ('TrackSuit', 'TrackSuit'),
    )
    currency = models.CharField(max_length=50, default='USD',
                                blank=True, null=True, choices=currency_type_choice)
    comments = models.TextField(max_length=3000, default='', blank=True, null=True)
    invoice_number = models.IntegerField(blank=True, null=True)
    invoice_date = models.DateTimeField(default=datetime.now)
    name = models.CharField('Customer Name', max_length=120, default='', blank=False, null=False)

    line_one = models.CharField('Line 1', max_length=120, default='',
                                blank=False, null=False, choices=product_type_choice)
    line_one_quantity = models.IntegerField('Quantity', default=0, blank=False, null=False)
    line_one_unit_price = models.IntegerField('Unit Price', default=0, blank=False, null=False)
    line_one_total_price = models.IntegerField('Line Total', default=0, blank=False, null=False)

    line_two = models.CharField('Line 2', max_length=120, default='',
                                blank=True, null=True, choices=product_type_choice)
    line_two_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_two_unit_price = models.IntegerField('Unit Price', default=0, blank=True, null=True)
    line_two_total_price = models.IntegerField('Line Total', default=0, blank=True, null=True)

    line_three = models.CharField('Line 3', max_length=120, default='',
                                  blank=True, null=True, choices=product_type_choice)
    line_three_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_three_unit_price = models.IntegerField('Unit Price', default=0, blank=True, null=True)
    line_three_total_price = models.IntegerField('Line Total', default=0, blank=True, null=True)

    line_four = models.CharField('Line 4', max_length=120, default='',
                                 blank=True, null=True, choices=product_type_choice)
    line_four_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_four_unit_price = models.IntegerField('Unit Price', default=0, blank=True, null=True)
    line_four_total_price = models.IntegerField('Line Total', default=0, blank=True, null=True)

    line_five = models.CharField('Line 5', max_length=120, default='',
                                 blank=True, null=True, choices=product_type_choice)
    line_five_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_five_unit_price = models.IntegerField('Unit Price', default=0, blank=True, null=True)
    line_five_total_price = models.IntegerField('Line Total', default=0, blank=True, null=True)

    line_six = models.CharField('Line 6', max_length=120, default='',
                                blank=True, null=True, choices=product_type_choice)
    line_six_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_six_unit_price = models.IntegerField('Unit Price', default=0, blank=True, null=True)
    line_six_total_price = models.IntegerField('Line Total', default=0, blank=True, null=True)

    line_seven = models.CharField('Line 7', max_length=120, default='',
                                  blank=True, null=True, choices=product_type_choice)
    line_seven_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_seven_unit_price = models.IntegerField('Unit Price', default=0, blank=True, null=True)
    line_seven_total_price = models.IntegerField('Line Total', default=0, blank=True, null=True)

    line_eight = models.CharField('Line 8', max_length=120, default='',
                                  blank=True, null=True, choices=product_type_choice)
    line_eight_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_eight_unit_price = models.IntegerField('Unit Price', default=0, blank=True, null=True)
    line_eight_total_price = models.IntegerField('Line Total', default=0, blank=True, null=True)

    line_nine = models.CharField('Line 9', max_length=120, default='',
                                 blank=True, null=True, choices=product_type_choice)
    line_nine_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_nine_unit_price = models.IntegerField('Unit Price', default=0, blank=True, null=True)
    line_nine_total_price = models.IntegerField('Line Total', default=0, blank=True, null=True)

    line_ten = models.CharField('Line 10', max_length=120, default='',
                                blank=True, null=True, choices=product_type_choice)
    line_ten_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_ten_unit_price = models.IntegerField('Unit Price', default=0, blank=True, null=True)
    line_ten_total_price = models.IntegerField('Line Total', default=0, blank=True, null=True)

    phone_number = models.CharField(max_length=120, default='', blank=True, null=True)
    total = models.IntegerField(default='0', blank=True, null=True)
    balance = models.IntegerField(default='0', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True)
    paid = models.BooleanField(default=False)
    invoice_type_choice = (
        ('Receipt', 'Receipt'),
        ('Proforma Invoice', 'Proforma Invoice'),
        ('Invoice', 'Invoice'),
    )
    invoice_type = models.CharField(max_length=50, default='Receipt',
                                    blank=True, null=True, choices=invoice_type_choice)
    confirmed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.invoice_number

    def get_absolute_url(self):
        return reverse('orders:single_sale', args=[self.id])
