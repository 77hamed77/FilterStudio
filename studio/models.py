from django.db import models
from django.contrib.auth.models import User
import os
import uuid 

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
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
    original_image = models.ImageField(upload_to=user_directory_path)
    processed_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    filter_applied = models.CharField(max_length=50, choices=FILTER_CHOICES)
    processing_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_filter_applied_display()} - {self.processing_date.strftime('%Y-%m-%d')}"
