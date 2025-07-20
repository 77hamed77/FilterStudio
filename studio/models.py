# studio/models.py
from django.db import models
from django.contrib.auth.models import User
import os
import uuid 

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4().hex}_{os.path.splitext(filename)[0][:30]}.{ext}"
    return f'uploads/{instance.user.username}/{unique_filename}'

# القائمة المحدثة مع كل الفلاتر، مصنفة حسب النوع (classic / ai)
FILTER_CHOICES_CLASSIFIED = [
    # فلاتر كلاسيكية
    {'value': 'original', 'name': 'الصورة الأصلية', 'type': 'classic'},
    {'value': 'crop', 'name': 'قص الصورة (تفاعلي)', 'type': 'classic'},
    {'value': 'grayscale', 'name': 'تحويل إلى الرمادي', 'type': 'classic'},
    {'value': 'invert', 'name': 'قلب الألوان', 'type': 'classic'},
    {'value': 'sharpen', 'name': 'زيادة الحدة (تفاعلي)', 'type': 'classic'},
    
    # فلاتر الذكاء الاصطناعي (تم حذف 'remove_background')
    {'value': 'blur_faces', 'name': 'طمس الوجوه (AI)', 'type': 'ai'},
    {'value': 'detect_human_face', 'name': 'التعرف على وجوه البشر (AI)', 'type': 'ai'},
    {'value': 'detect_cat_face', 'name': 'التعرف على وجوه القطط (AI)', 'type': 'ai'},
    {'value': 'detect_eyes', 'name': 'التعرف على العيون (AI)', 'type': 'ai'},
    {'value': 'detect_smile', 'name': 'التعرف على الابتسامات (AI)', 'type': 'ai'},
    {'value': 'detect_full_body', 'name': 'التعرف على كامل الجسد (AI)', 'type': 'ai'},
    {'value': 'detect_upper_body', 'name': 'التعرف على الجزء العلوي من الجسد (AI)', 'type': 'ai'},
    {'value': 'detect_license_plate', 'name': 'التعرف على لوحات السيارات (AI)', 'type': 'ai'},
]

# دالة مساعدة للحصول على الخيارات بتنسيق Django (value, name)
def get_filter_choices_for_model():
    return [(f['value'], f['name']) for f in FILTER_CHOICES_CLASSIFIED]

class ProcessedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to=user_directory_path)
    processed_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    filter_applied = models.CharField(max_length=50, choices=get_filter_choices_for_model()) 
    processing_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_filter_applied_display()} - {self.processing_date.strftime('%Y-%m-%d')}"

    def delete(self, *args, **kwargs):
        if self.original_image:
            self.original_image.delete(save=False)
        if self.processed_image:
            self.processed_image.delete(save=False)
        super().delete(*args, **kwargs)