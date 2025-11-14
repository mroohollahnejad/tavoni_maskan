from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeView
from .views import (
    CustomLoginView, dashboard,profile_edit,
payment_create_ajax, payment_edit_ajax, payment_delete_ajax, score_ajax,
    upload_members_and_payments, download_sample_excel
)

urlpatterns = [
    # ----------------- صفحات اصلی -----------------
    path('', dashboard, name='dashboard'),
    path('dashboard/', dashboard, name='dashboard'),

    # ----------------- ورود -----------------
    path('login/', CustomLoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('login/member/', CustomLoginView.as_view(template_name='accounts/member_login.html'), name='member_login'),
    path('upload-members', CustomLoginView.as_view(template_name='accounts/upload_login.html'), name='upload_login'),
    path('login/admin/', CustomLoginView.as_view(template_name='accounts/admin_login.html'), name='admin_login'),

    # ----------------- خروج -----------------
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # ----------------- پروفایل -----------------
    path('profile/edit/', profile_edit, name='profile_edit'),
    path(
        'password_change/',
        PasswordChangeView.as_view(
            template_name='accounts/password_change.html',
            success_url='/dashboard/'
        ),
        name='password_change'
    ),
    # ----------------- مسیرهای AJAX -----------------
    path('payments/create/', payment_create_ajax, name='payment_create_ajax'),
    path('payments/<int:pk>/edit/', payment_edit_ajax, name='payment_edit_ajax'),
    path('payments/<int:pk>/delete/', payment_delete_ajax, name='payment_delete_ajax'),
    path('payments/score/', score_ajax, name='score_ajax'),
    # ----------------- آپلود اکسل -----------------
    path('upload-members/', upload_members_and_payments, name='upload_members_and_payments'),
    path('download-sample-excel/', download_sample_excel, name='download_sample_excel'),
]
