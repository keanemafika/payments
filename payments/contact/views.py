from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


def teachers(request):
    return render(request, "contact/teachers.html")


def about(request):
    return render(request, "contact/about.html")


def pricing(request):
    return render(request, "contact/pricing.html")


def pre_school(request):
    return render(request, "contact/pre-school.html")


def daycare(request):
    return render(request, "contact/daycare.html")


def primary_school(request):
    return render(request, "contact/primary-school.html")


def contact(request):
    if request.method == "POST":
        subject = 'Subject: ' + request.POST['subject']
        from_email = request.POST['email']
        name = request.POST['name']
        message = 'Message:' + request.POST['message'] + '. email:' + request.POST['email'] + \
            '. Name:' + request.POST['name'] + '. Phone#:' + request.POST['phone']

        # send Email
        send_mail(subject, message, from_email, ['wascgos@gmail.com'], fail_silently=False,)
        messages.success(request, 'Thank you ' + name + ' (' + from_email + ')' + ' for contacting us. we will get back to you as soon as possible.')

        return HttpResponseRedirect(reverse('contact:contact'))

    else:
        return render(request, "contact/contact.html")
