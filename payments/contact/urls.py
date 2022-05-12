from django.urls import path

from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact, name='contact'),
    path('pricing/', views.pricing, name='pricing'),
    path('teachers/', views.teachers, name='teachers'),
    path('about-us/', views.about, name='about'),
    path('pre-school/', views.pre_school, name='pre_school'),
    path('daycare/', views.daycare, name='daycare'),
    path('primary-school/', views.primary_school, name='primary_school'),
]
