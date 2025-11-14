from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_jalali.db import models as jmodels  # برای تاریخ شمسی

# مدل پروفایل کاربر
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login_count = models.IntegerField(default=0)

    # اطلاعات شخصی
    first_name = models.CharField(max_length=50, blank=True, verbose_name="نام")
    last_name = models.CharField(max_length=50, blank=True, verbose_name="نام خانوادگی")
    national_code = models.CharField(max_length=10, blank=True, verbose_name="شماره ملی")
    birth_certificate = models.CharField(max_length=10, blank=True, verbose_name="شماره شناسنامه")
    phone_number = models.CharField(max_length=11, blank=True, verbose_name="شماره همراه")
    birth_date = jmodels.jDateField(blank=True, null=True, verbose_name="تاریخ تولد (شمسی)")
    birth_place = models.CharField(max_length=100, blank=True, verbose_name="محل تولد")

    # عکس پروفایل
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return f"{self.user.username} Profile"


# مدل واریزی‌ها (قابل ثبت چندبار برای هر نوبت)
PAYMENT_CHOICES = [(i, f"نوبت واریزی {i}") for i in range(1, 11)]

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    installment_number = models.IntegerField(choices=PAYMENT_CHOICES, verbose_name="نوبت واریز")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="مبلغ واریزی")
    payment_date = jmodels.jDateField(verbose_name="تاریخ واریز (شمسی)")
    due_date = models.DateField(blank=True, null=True)  # ستون جدید
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['installment_number', 'payment_date']  # مرتب‌سازی پیش‌فرض
        verbose_name = "واریز"
        verbose_name_plural = "واریزی‌ها"

    def __str__(self):
        return f"{self.user.username} - نوبت {self.installment_number} - مبلغ {self.amount}"


# سیگنال‌های ایجاد خودکار پروفایل
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

class ApprovedPaymentDate(models.Model):
    installment_number = models.PositiveSmallIntegerField(unique=True)
    due_date = models.DateField()

    class Meta:
        ordering = ['installment_number']

    def __str__(self):
        return f"نوبت {self.installment_number} - {self.due_date}"
