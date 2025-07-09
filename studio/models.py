# studio/models.py (النسخة المصححة)

from django.db import models
from django.contrib.auth.models import User
import os
import uuid # <-- إضافة هذا الاستيراد

def user_directory_path(instance, filename):
    # الحصول على امتداد الملف الأصلي
    ext = filename.split('.')[-1]
    # إنشاء اسم ملف فريد باستخدام UUID وإعادة اسم الملف الأصلي قبل الامتداد
    # هذا يضمن تفرد اسم الملف مع الحفاظ على جزء من الاسم الأصلي لسهولة التعرف
    unique_filename = f"{uuid.uuid4().hex}_{os.path.splitext(filename)[0][:30]}.{ext}"
    return f'uploads/{instance.user.username}/{unique_filename}'

# القائمة المحدثة مع كل الفلاتر
FILTER_CHOICES = [
    ('original', 'الصورة الأصلية'),
    ('crop', 'قص الصورة (تفاعلي)'),
    ('grayscale', 'تحويل إلى الرمادي'),
    ('invert', 'قلب الألوان'),
    ('sharpen', 'زيادة الحدة (تفاعلي)'),
    ('blur_faces', 'طمس الوجوه (تفاعلي)'),
    ('remove_background', 'إزالة الخلفية'),
    ('detect_human_face', 'التعرف على وجوه البشر'),
    ('detect_cat_face', 'التعرف على وجوه القطط'),
    ('detect_eyes', 'التعرف على العيون'),
    ('detect_smile', 'التعرف على الابتسامات'),
    ('detect_full_body', 'التعرف على كامل الجسد'),
    ('detect_upper_body', 'التعرف على الجزء العلوي من الجسد'),
    ('detect_license_plate', 'التعرف على لوحات السيارات'),
]

class ProcessedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # كلا الحقلين original_image و processed_image سيستخدمان الآن DEFAULT_FILE_STORAGE
    # الذي تم تعيينه إلى S3Boto3Storage في settings.py
    original_image = models.ImageField(upload_to=user_directory_path)
    processed_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    filter_applied = models.CharField(max_length=50, choices=FILTER_CHOICES)
    processing_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_filter_applied_display()} - {self.processing_date.strftime('%Y-%m-%d')}"

    # ✅ ملاحظة: تأكد من أن لديك دالة delete هنا (أو في مكان آخر)
    # لحذف الملفات من Supabase Storage عند حذف الكائن.
    # إذا كانت موجودة في نسخة سابقة، فاحتفظ بها.
    # مثال:
    # def delete(self, *args, **kwargs):
    #     self.original_image.delete(save=False)
    #     if self.processed_image:
    #         self.processed_image.delete(save=False)
    #     super().delete(*args, **kwargs)