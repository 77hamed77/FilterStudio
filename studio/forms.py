# studio/forms.py (النسخة المصححة لخطأ KeyError)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# كلاسات Tailwind CSS التي نريد تطبيقها
INPUT_CLASSES = 'w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent transition'

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label='الاسم الأول',
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'أدخل اسمك الأول'})
    )
    last_name = forms.CharField(
        label='اسم العائلة',
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'أدخل اسم عائلتك'})
    )
    email = forms.EmailField(
        label='البريد الإلكتروني',
        required=True,
        widget=forms.EmailInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'أدخل بريدك الإلكتروني'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # تطبيق الكلاسات على الحقول الافتراضية
        self.fields['username'].widget.attrs.update({'class': INPUT_CLASSES, 'placeholder': 'اختر اسم مستخدم'})
        
        # ==================== الجزء الذي تم إصلاحه ====================
        # ✅ الإصلاح: تم تغيير اسم الحقل من 'password' إلى 'password1'
        self.fields['password1'].widget.attrs.update({'class': INPUT_CLASSES, 'placeholder': 'أدخل كلمة مرور قوية'})
        self.fields['password2'].widget.attrs.update({'class': INPUT_CLASSES, 'placeholder': 'أعد إدخال كلمة المرور'})
        # ==================== نهاية الجزء المعدل ====================