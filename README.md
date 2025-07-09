<div align="center">

# ✨ FilterStudio ✨

**تطبيق ويب متكامل لمعالجة الصور باستخدام Django و OpenCV، مع واجهة مستخدم عصرية وميزات مدعومة بالذكاء الاصطناعي.**

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img alt="Django" src="https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white"/>
  <img alt="OpenCV" src="https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"/>
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge"/>
</p>

[<img src="https://img.shields.io/badge/Live_Demo-Visit_Site-28a745?style=for-the-badge&logo=render" />](https://filterstudio.onrender.com/)

</div>

---

## 📸 معرض المشروع (Project Showcase)

للحصول على أفضل انطباع، يرجى زيارة النسخة الحية من المشروع. يمكنك أيضاً مشاهدة هذا العرض السريع للواجهة الرئيسية:

[![FilterStudio Demo](https://i.imgur.com/uGkF9iR.png)](https://filterstudio.onrender.com/)


---

## 🚀 الميزات الرئيسية (Key Features)

يقدم FilterStudio مجموعة متكاملة من الأدوات التي تلبي احتياجات المصممين والمصورين:

*   **🔐 نظام مستخدمين آمن:**
    *   تسجيل حساب جديد، تسجيل دخول وخروج.
    *   استوديو شخصي لكل مستخدم لعرض وإدارة صوره الخاصة.

*   **⚡️ معاينة حية وتفاعلية:**
    *   شاهد تأثير الفلاتر على صورتك **مباشرةً** قبل الحفظ، مما يوفر تجربة استخدام سلسة وسريعة.

*   **🎨 فلاتر كلاسيكية وتفاعلية:**
    *   **القص والتدوير:** تحكم كامل بأبعاد الصورة باستخدام أداة `Cropper.js` الاحترافية.
    *   **الحدة والتعتيم:** أشرطة تمرير دقيقة للتحكم بقوة فلتر Sharpen وفلتر Blur.
    *   **أساسيات الألوان:** فلاتر التدرج الرمادي (Grayscale) وعكس الألوان (Invert).

*   **🧠 فلاتر كشف ذكية (OpenCV):**
    *   **كشف دقيق لوجوه البشر:** باستخدام نموذج `haarcascade_frontalface_alt2.xml` المحسّن.
    *   **كشف متقدم:** التعرف على وجوه القطط، العيون، والابتسامات باستخدام منطق البحث داخل الوجه لزيادة الدقة.
    *   **كشف الأجسام:** التعرف على كامل الجسد، الجزء العلوي منه، ولوحات السيارات.

---

## 🛠️ التقنيات المستخدمة (Tech Stack)

تم بناء هذا المشروع باستخدام مجموعة من التقنيات الحديثة والقوية:

| الفئة | التقنية |
|---|---|
| **الواجهة الخلفية (Backend)** | ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Django](https://img.shields.io/badge/-Django-092E20?style=flat-square&logo=django&logoColor=white) |
| **الواجهة الأمامية (Frontend)** | ![HTML5](https://img.shields.io/badge/-HTML5-E34F26?style=flat-square&logo=html5&logoColor=white) ![TailwindCSS](https://img.shields.io/badge/-Tailwind_CSS-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white) ![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black) |
| **معالجة الصور** | ![OpenCV](https://img.shields.io/badge/-OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white) ![Pillow](https://img.shields.io/badge/-Pillow-a8a8a8?style=flat-square) |
| **قاعدة البيانات** | ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white) ![Supabase](https://img.shields.io/badge/-Supabase-3ECF8E?style=flat-square&logo=supabase&logoColor=white) |
| **تخزين الملفات** | ![Supabase Storage](https://img.shields.io/badge/-Supabase_Storage-3ECF8E?style=flat-square&logo=supabase&logoColor=white) |
| **النشر (Deployment)** | ![Render](https://img.shields.io/badge/-Render-46E3B7?style=flat-square&logo=render&logoColor=white) |
| **أدوات إضافية** | Cropper.js |

---

## ⚙️ التشغيل محلياً (Local Setup)

لتشغيل المشروع على جهازك المحلي، اتبع الخطوات التالية:

1.  **نسخ المستودع (Clone the repository):**
    ```bash
    git clone https://github.com/77hamed77/FilterStudio.git
    cd FilterStudio
    ```

2.  **إنشاء وتفعيل البيئة الافتراضية (Create and activate virtual environment):**
    ```bash
    python -m venv venv
    # For Windows
    venv\Scripts\activate
    # For macOS/Linux
    source venv/bin/activate
    ```

3.  **تثبيت المكتبات (Install dependencies):**
    ```bash
    pip install -r requirements.txt
    ```

4.  **إعداد متغيرات البيئة (Set up environment variables):**
    *   أنشئ ملفاً باسم `.env` في جذر المشروع.
    *   أضف المتغيرات التالية إلى الملف مع قيمك الخاصة:
    ```env
    SECRET_KEY=your_django_secret_key
    DATABASE_URL=your_supabase_postgres_connection_url
    CLOUDINARY_URL=your_supabase_storage_or_other_storage_url
    ```

5.  **تطبيق التحديثات على قاعدة البيانات (Apply migrations):**
    ```bash
    python manage.py migrate
    ```

6.  **تشغيل الخادم (Run the server):**
    ```bash
    python manage.py runserver
    ```
    الآن يمكنك زيارة الموقع على `https://filterstudio.onrender.com`.

---

## 📜 الترخيص (License)

هذا المشروع مرخص تحت رخصة MIT. انظر ملف `LICENSE` للمزيد من التفاصيل.

---

## 👨‍💻 المؤلف (Author)

**حامد محمد المرعي**

<p>
    <a href="https://github.com/77hamed77" target="_blank">
        <img alt="Github" src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white">
    </a>
    <a href="https://www.linkedin.com/in/hamidmuhammad/" target="_blank">
        <img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white">
    </a>
</p>