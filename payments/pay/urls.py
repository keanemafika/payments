from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from pay.views import PaymentView, PrintReceipt, ViewPDF, DownloadPDF, ClearStudentView, EditPayment, DeletePayment, ConfirmPayment, CompleteProfile, EditStudentDetails


app_name = 'pay'
urlpatterns = [
    path('', views.payments, name='home'),
    path('make-payment', PaymentView.as_view(), name='make_payment'),
    path('confirm-payment/<int:pk>', ConfirmPayment.as_view(), name='confirm_payment'),
    path('all-transactions', views.all_transactions, name='all_transactions'),
    path('check-status', views.check_status, name='check_status'),
    path('class-status/<slug>', views.classroom_status, name='classroom_status'),
    path('print-receipt/<int:pk>/', PrintReceipt.as_view(), name='print_receipt'),
    path('pdf_view/<int:pk>', ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/<int:pk>', DownloadPDF.as_view(), name="pdf_download"),
    path('clear-student/<int:pk>', ClearStudentView.as_view(), name="clear_student"),
    path('edit-payment/<int:pk>', EditPayment.as_view(), name="edit_payment"),
    path('delete-payment/<int:pk>', DeletePayment.as_view(), name="delete_payment"),
    path('student-details/<username>', views.single_student_details, name='single_student_details'),
    path('edit-student-details/<int:pk>', EditStudentDetails.as_view(), name='edit_student_details'),
    path('contact-upload/', views.contact_upload, name='contact_upload'),
    path('profile-upload/', views.profile_upload, name='profile_upload'),
    path('groceries-upload/', views.groceries_upload, name='groceries_upload'),
    path('tuition-upload/', views.tuition_upload, name='tuition_upload'),
    path('clearance-upload/', views.clearance_upload, name='clearance_upload'),
    path('enrol-student/', views.enrol_student, name='enrol_student'),
    path('complete-enrol-profile/<int:pk>', CompleteProfile.as_view(), name='complete_profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)
