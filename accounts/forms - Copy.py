from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .models import Payment

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name', 'last_name', 'national_code',
            'birth_certificate', 'phone_number', 'birth_date', 'birth_place'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}),
            'national_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره ملی'}),
            'birth_certificate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره شناسنامه'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره همراه'}),
            'birth_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'تاریخ تولد شمسی (مثلاً 1402-07-20)'}),
            'birth_place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'محل تولد'}),
        }

from django import forms
from .models import Payment
import jdatetime
from datetime import date

class PaymentForm(forms.ModelForm):
    payment_date = forms.CharField(label="تاریخ پرداخت", required=True)

    class Meta:
        model = Payment
        fields = ['installment_number', 'amount', 'payment_date']

    def clean_payment_date(self):
        date_str = self.cleaned_data['payment_date'].strip()

        # تلاش برای تشخیص تاریخ شمسی یا میلادی
        try:
            # حالت اول: تاریخ شمسی مثل 1404/07/01
            if '/' in date_str and int(date_str.split('/')[0]) > 1300:
                jdate = jdatetime.date.fromisoformat(date_str.replace('/', '-'))
                return jdate.togregorian()

            # حالت دوم: تاریخ میلادی مثل 2025-10-28 یا 2025/10/28
            date_str = date_str.replace('/', '-')
            y, m, d = map(int, date_str.split('-'))
            return date(y, m, d)

        except Exception:
            raise forms.ValidationError("تاریخ وارد شده معتبر نیست. از فرمت 1404/07/01 یا 2025-10-28 استفاده کنید.")