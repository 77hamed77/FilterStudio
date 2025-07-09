# filter_studio/urls.py (النسخة الصحيحة)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ✅ هذا هو السطر الأهم:
    # إنه يخبر Django أن يتعامل مع أي رابط لا يبدأ بـ 'admin/'
    # باستخدام ملف الروابط الخاص بتطبيق 'studio'.
    path('', include('studio.urls')), 
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)