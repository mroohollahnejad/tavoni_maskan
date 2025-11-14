from django import forms
from django.contrib.auth.models import User
from .models import Profile
import jdatetime
from datetime import date
from .models import Payment, ApprovedPaymentDate


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



class MembersUploadForm(forms.Form):
    file = forms.FileField(label="انتخاب فایل Excel اعضا و پرداخت‌ها")


class PaymentForm(forms.ModelForm):
    payment_date = forms.CharField(label="تاریخ واریز", widget=forms.TextInput(attrs={'class':'form-control'}))
    due_date = forms.CharField(label="تاریخ مصوب", required=False, widget=forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}))
    installment_number = forms.ChoiceField(label="نوبت واریزی", widget=forms.Select(attrs={'class':'form-select'}))

    class Meta:
        model = Payment
        fields = ['installment_number','due_date','amount','payment_date']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        approved_dates = ApprovedPaymentDate.objects.all()
        if approved_dates.exists():
            self.fields['installment_number'].choices = [(p.installment_number,f"نوبت {p.installment_number}") for p in approved_dates]
        else:
            self.fields['installment_number'].choices = [(i,f"نوبت {i}") for i in range(1,13)]

        if self.instance and self.instance.pk:
            try:
                due = ApprovedPaymentDate.objects.get(installment_number=self.instance.installment_number)
                self.fields['due_date'].initial = due.due_date
            except ApprovedPaymentDate.DoesNotExist:
                self.fields['due_date'].initial = ''

    def clean_payment_date(self):
        date_str = self.cleaned_data['payment_date'].strip()
        try:
            if '/' in date_str and int(date_str.split('/')[0])>1300:
                jdate = jdatetime.date.fromisoformat(date_str.replace('/','-'))
                return jdate.togregorian()
            y,m,d = map(int,date_str.replace('/','-').split('-'))
            return date(y,m,d)
        except:
            raise forms.ValidationError("تاریخ معتبر نیست")

    def clean(self):
        cleaned_data = super().clean()
        installment = int(cleaned_data.get('installment_number'))
        try:
            due = ApprovedPaymentDate.objects.get(installment_number=installment)
            cleaned_data['due_date'] = due.due_date
        except ApprovedPaymentDate.DoesNotExist:
            cleaned_data['due_date'] = ''
        return cleaned_data
