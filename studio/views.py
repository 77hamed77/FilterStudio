# studio/views.py
import os
import cv2
import numpy as np
import base64
from django.conf import settings
from django.http import JsonResponse, HttpResponse # إضافة HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
# استيراد FILTER_CHOICES_CLASSIFIED بدلاً من FILTER_CHOICES
from .models import ProcessedImage, FILTER_CHOICES_CLASSIFIED, user_directory_path 
from .forms import CustomUserCreationForm

# 🔴 تم حذف استيراد rembg بالكامل
# from rembg import remove

CASCADE_FILES = {
    'human_face': 'haarcascade_frontalface_alt2.xml',
    'cat_face': 'haarcascade_frontalcatface.xml',
    'eyes': 'haarcascade_eye.xml',
    'smile': 'haarcascade_smile.xml',
    'full_body': 'haarcascade_fullbody.xml',
    'upper_body': 'haarcascade_upperbody.xml',
    'license_plate': 'haarcascade_license_plate_rus_16stages.xml'
}
CASCADES = {}
print("--- بدء تحميل نماذج Haar Cascade ---")
for name, filename in CASCADE_FILES.items():
    path = os.path.join(settings.BASE_DIR, 'static', 'haarcascades', filename)
    if os.path.exists(path):
        CASCADES[name] = cv2.CascadeClassifier(path)
        if CASCADES[name].empty(): print(f"!!! خطأ: فشل تحميل '{filename}'")
        else: print(f"    - تم تحميل '{filename}' بنجاح.")
    else:
        print(f"!!! خطأ فادح: الملف '{filename}' غير موجود. يرجى التحقق من مسار static/haarcascades.")
        CASCADES[name] = None
print("--- اكتمل تحميل النماذج ---")

DETECTION_PARAMS = {
    'human_face': {'scaleFactor': 1.1, 'minNeighbors': 6, 'minSize': (40, 40)},
    'cat_face': {'scaleFactor': 1.1, 'minNeighbors': 4, 'minSize': (50, 50)},
    'smile': {'scaleFactor': 1.7, 'minNeighbors': 22, 'minSize': (25, 25)},
    'eyes': {'scaleFactor': 1.1, 'minNeighbors': 10, 'minSize': (20, 20)},
    'default': {'scaleFactor': 1.1, 'minNeighbors': 5, 'minSize': (30, 30)},
}

# ✅ تم حذف original_buffer من تعريف الدالة لأنه لم يعد يستخدم لـ rembg
def apply_cv_filter(img, filter_type, params=None): 
    if params is None: params = {}
    processed = img.copy()
    info_message = ""
    
    # 🔴 تم حذف منطق 'remove_background' بالكامل
    
    if filter_type == 'blur_faces':
        cascade = CASCADES.get('human_face')
        if cascade and not cascade.empty():
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = cascade.detectMultiScale(gray, **DETECTION_PARAMS['human_face'])
            blur_level = int(params.get('blur_level', 10))
            if blur_level % 2 == 0: blur_level += 1
            kernel_size = (blur_level, blur_level) 
            for (x, y, w, h) in faces:
                if w > 0 and h > 0:
                    processed[y:y+h, x:x+w] = cv2.GaussianBlur(processed[y:y+h, x:x+w], kernel_size, 0)
            info_message = f'تم تعتيم {len(faces)} وجه.'
        else:
            info_message = "خطأ: نموذج كشف الوجوه غير متوفر."
    elif filter_type == 'grayscale':
        processed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif filter_type == 'invert':
        processed = cv2.bitwise_not(img)
    elif filter_type == 'crop':
        x, y, w, h = params.get('x',0), params.get('y',0), params.get('w',0), params.get('h',0)
        if w > 0 and h > 0:
            y_max, x_max = img.shape[:2]
            x = max(0, min(x, x_max))
            y = max(0, min(y, y_max))
            w = max(0, min(w, x_max - x))
            h = max(0, min(h, y_max - y))
            if w > 0 and h > 0:
                processed = img[y:y+h, x:x+w]
            else:
                info_message = "أبعاد القص غير صالحة."
                processed = img.copy()
        else:
            info_message = "يرجى تحديد منطقة القص."
            processed = img.copy()
    elif filter_type == 'sharpen':
        level = params.get('level', 5.5)
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        processed = cv2.filter2D(img, -1, kernel)
    elif filter_type in ['detect_smile', 'detect_eyes']:
        human_face_cascade = CASCADES.get('human_face')
        feature_name = filter_type.split('_')[1]
        feature_cascade = CASCADES.get(feature_name)
        if human_face_cascade and feature_cascade and not human_face_cascade.empty() and not feature_cascade.empty():
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = human_face_cascade.detectMultiScale(gray, **DETECTION_PARAMS['human_face'])
            detected_items_count = 0
            for (x, y, w, h) in faces:
                cv2.rectangle(processed, (x, y), (x+w, y+h), (255, 0, 0), 2)
                face_roi_gray = gray[y:y+h, x:x+w]
                face_roi_color = processed[y:y+h, x:x+w]
                
                min_size_feature = DETECTION_PARAMS[feature_name]['minSize']
                
                features = feature_cascade.detectMultiScale(
                    face_roi_gray, 
                    scaleFactor=DETECTION_PARAMS[feature_name]['scaleFactor'],
                    minNeighbors=DETECTION_PARAMS[feature_name]['minNeighbors'],
                    minSize=min_size_feature
                )
                for (fx, fy, fw, fh) in features:
                    cv2.rectangle(face_roi_color, (fx, fy), (fx+fw, fy+fh), (0, 255, 0), 2)
                    detected_items_count += 1
            info_message = f'عدد الوجوه المكتشفة: {len(faces)}، عدد الميزات المكتشفة: {detected_items_count}'
        else:
            info_message = "خطأ: نماذج الكشف عن الوجه/الميزة غير متوفرة."
    elif filter_type.startswith('detect_'):
        cascade_name = filter_type.replace('detect_', '')
        cascade = CASCADES.get(cascade_name)
        if cascade and not cascade.empty():
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            params_detect = DETECTION_PARAMS.get(cascade_name, DETECTION_PARAMS['default'])
            objects = cascade.detectMultiScale(gray, **params_detect)
            for (x, y, w, h) in objects:
                cv2.rectangle(processed, (x, y), (x+w, y+h), (0, 255, 0), 3)
            info_message = f'عدد الكائنات المكتشفة: {len(objects)}'
        else:
            info_message = f"خطأ: نموذج الكشف عن {cascade_name} غير متوفر."
    else:
        info_message = "لا يوجد فلتر أو فلتر غير مدعوم."
        processed = img.copy()

    if processed.ndim == 2:
        processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
    
    return processed, info_message

# --- دالة عرض جديدة للمعاينات الحية ---
@login_required
def preview_filter_view(request):
    if request.method != 'POST': return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    try:
        image_data_url = request.POST.get('image_data')
        filter_type = request.POST.get('filter_type')
        
        if not image_data_url or not filter_type:
            return JsonResponse({'error': 'بيانات الصورة أو نوع الفلتر مفقود'}, status=400)

        params = {
            'level': float(request.POST.get('sharpen_level') or 5.5),
            'blur_level': float(request.POST.get('blur_level') or 10),
        }
        
        if filter_type == 'crop':
            params['x'] = int(float(request.POST.get('crop_x') or 0))
            params['y'] = int(float(request.POST.get('crop_y') or 0))
            params['w'] = int(float(request.POST.get('crop_width') or 0))
            params['h'] = int(float(request.POST.get('crop_height') or 0))

        format, imgstr = image_data_url.split(';base64,') 
        img_data = base64.b64decode(imgstr)
        img_array = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            return JsonResponse({'error': 'تعذر قراءة ملف الصورة للمعاينه.'}, status=400)

        # ✅ تم حذف original_buffer من هنا
        processed_img, info_message = apply_cv_filter(img, filter_type, params)
        
        if len(processed_img.shape) == 2:
            processed_img = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2BGR)
        
        # ✅ تبسيط: دائماً نُعيد JPEG للمعاينة (بما أننا حذفنا rembg)
        _, buffer = cv2.imencode('.jpeg', processed_img) 
        mime_type = 'image/jpeg'

        processed_img_str = base64.b64encode(buffer).decode('utf-8')
        
        return JsonResponse({'image': f'data:{mime_type};base64,' + processed_img_str, 'message': info_message})
    except Exception as e:
        print(f"Error in preview: {e}")
        return JsonResponse({'error': f'فشل في المعاينة: {e}'}, status=500)

# --- دالة الرفع الرئيسية ---
@login_required
def upload_view(request):
    context = {
        'filter_choices_classified': FILTER_CHOICES_CLASSIFIED,
        'classic_filters': [f for f in FILTER_CHOICES_CLASSIFIED if f['type'] == 'classic'],
        'ai_filters': [f for f in FILTER_CHOICES_CLASSIFIED if f['type'] == 'ai'],
    }
    if request.method != 'POST': 
        return render(request, 'studio/upload.html', context)

    image_file = request.FILES.get('image')
    filter_type = request.POST.get('filter')

    if not image_file:
        messages.error(request, 'يرجى اختيار صورة.')
        return redirect('upload')
    
    valid_filters = [f['value'] for f in FILTER_CHOICES_CLASSIFIED]
    if filter_type not in valid_filters:
        messages.error(request, 'فلتر غير صالح.')
        return redirect('upload')

    try:
        img_buffer = image_file.read()
        img_array = np.frombuffer(img_buffer, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if img is None:
            messages.error(request, 'تعذر قراءة ملف الصورة.')
            return redirect('upload')

        params = {
            'x': int(float(request.POST.get('crop_x') or 0)),
            'y': int(float(request.POST.get('crop_y') or 0)),
            'w': int(float(request.POST.get('crop_width') or 0)),
            'h': int(float(request.POST.get('crop_height') or 0)),
            'level': float(request.POST.get('sharpen_level') or 5.5),
            'blur_level': float(request.POST.get('blur_level') or 10),
        }

        # ✅ تم حذف original_buffer من هنا
        processed, info_message = apply_cv_filter(img, filter_type, params)

        # ✅ تبسيط: دائماً نُعيد JPG للحفظ (بما أننا حذفنا rembg)
        if len(processed.shape) == 2:
            processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
        
        ext, encoder = '.jpg', cv2.imencode('.jpg', processed)[1]
        
        original_file_name_base, _ = os.path.splitext(image_file.name)
        processed_filename = f'processed_{original_file_name_base}{ext}'
        
        new_image = ProcessedImage(user=request.user, original_image=image_file, filter_applied=filter_type)
        
        processed_file_content = ContentFile(encoder.tobytes())
        new_image.processed_image.save(processed_filename, processed_file_content, save=True)

        if info_message: messages.info(request, info_message)
        messages.success(request, 'تم تطبيق الفلتر ورفع الصورة بنجاح!')
        return redirect('studio')

    except Exception as e:
        print(f"!!!!!!!!!! حدث خطأ في upload_view: {e} !!!!!!!!!!")
        messages.error(request, f'حدث خطأ غير متوقع أثناء معالجة الصورة: {e}')
        return redirect('upload')

# --- دوال المصادقة والعرض الأخرى (لا تحتاج لتعديل) ---
def home_view(request):
    return render(request, 'studio/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('studio')
        else:
            try: User.objects.get(username=username)
            except User.DoesNotExist: messages.error(request, 'اسم المستخدم غير موجود.')
            else: messages.error(request, 'كلمة المرور غير صحيحة.')
    return render(request, 'studio/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
    
@login_required
def studio_view(request):
    images = ProcessedImage.objects.filter(user=request.user).order_by('-processing_date')
    return render(request, 'studio/studio.html', {'images': images})

@login_required
def image_detail_view(request, image_id):
    image = get_object_or_404(ProcessedImage, id=image_id, user=request.user)
    return render(request, 'studio/image_detail.html', {'image': image})

@login_required
def delete_image_view(request, image_id):
    image = get_object_or_404(ProcessedImage, id=image_id, user=request.user)
    if request.method == "POST":
        image.delete()
        messages.success(request, "تم حذف الصورة بنجاح.")
        return redirect('studio')
    return render(request, 'studio/confirm_delete.html', {'image': image})
    
def register_view(request):
    if request.user.is_authenticated:
        return redirect('studio')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم التسجيل بنجاح. يمكنك تسجيل الدخول الآن.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                label = form.fields.get(field).label if form.fields.get(field) else field.replace('_', ' ').title()
                for error in errors: messages.error(request, f"{label}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'studio/register.html', {'form': form})
    
@login_required
def account_settings_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'تم تحديث كلمة المرور بنجاح.')
            return redirect('account_settings')
        else:
            for field, errors in form.errors.items():
                label = form.fields.get(field).label if form.fields.get(field) else field.replace('_', ' ').title()
                for error in errors: messages.error(request, f"{label}: {error}")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'studio/account_settings.html', {'form': form})